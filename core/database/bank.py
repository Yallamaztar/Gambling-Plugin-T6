from typing import Dict, List, Optional
from threading import RLock
import json, os

class BankManager:
    _instance: Optional["BankManager"] = None
    
    def __new__(cls) -> "BankManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            print("[BankManager] Creating new instance")
        return cls._instance
    
    def __init__(self):
        if hasattr(self, 'initialized'):
            return
            
        database  = os.path.dirname(os.path.abspath(__file__))
        self.bank_db = os.path.join(database, "data", "bank.json")
        os.makedirs(os.path.dirname(self.bank_db), exist_ok=True)
        
        self.lock = RLock()
        self.bank = self.load()
        self.initialized = True
        print("[BankManager] Database initialized")

    def load(self) -> Dict[str, int]:
        with self.lock:
            try:
                with open(self.bank_db, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
            
    def save(self) -> None:
        with self.lock:
            with open(self.bank_db, 'w', encoding='utf-8') as f:
                json.dump(self.bank, f, indent=2)

    def balance(self, player: str) -> int:
        with self.lock:
            return self.bank.get(player, 0)
    
    def deposit(self, player: str, amount: int) -> None:
        with self.lock:
            self.bank[player] = self.bank.get(player, 0) + amount
            self.save()

    def reset(self) -> None:
        with self.lock:
            self.bank.clear()
            self.save()

    def top_balances(self, count: Optional[int] = 5) -> List[Dict[str, str | int]]:
        with self.lock:
            return [
                {'name': player, 'balance': balance} 
                for player, balance in sorted(self.bank.items(), key=lambda item: item[1], reverse=True)[:count]
            ]
        
    def __enter__(self) -> "BankManager":
        self.lock.acquire()
        return self