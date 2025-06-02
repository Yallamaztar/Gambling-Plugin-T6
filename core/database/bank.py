from typing import Dict, List, Optional
from threading import RLock
import json, os

from core.utils import safe_int

class BankManager:
    def __init__(self):
        database  = os.path.dirname(os.path.abspath(__file__))
        self.bank_db = os.path.join(database, "data", "bank.json")
        os.makedirs(os.path.dirname(self.bank_db), exist_ok=True)
        
        self.lock = RLock()
        self.bank = self.load()

    def load(self) -> Dict[str, int]:
        with self.lock:
            try:
                with open(self.bank_db, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
            
    def save(self) -> None:
        with self.lock:
            with open(self.bank_db, 'w') as f:
                json.dump(self.bank, f, indent=2)

    def balance(self, player: str) -> int:
        with self.lock:
            return self.bank.get(player, 0)
    
    def deposit(self, player: str, amount: int) -> None:
        with self.lock:
            self.bank[player] = safe_int(self.balance(player)) + safe_int(amount)
            self.save()

    def reset(self) -> None:
        with self.lock:
            self.bank.clear()
            self.save()

    def top_balances(self, count: Optional[int] = 5) -> List[Dict[str, int]]:
        with self.lock:
            return [
                {'name': player, 'balance': balance} 
                for player, balance in sorted(self.bank.items(), key=lambda item: item[1], reverse=True)[:count]
            ]