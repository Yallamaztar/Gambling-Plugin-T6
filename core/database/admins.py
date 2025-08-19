from typing import Optional, List, Union
from threading import RLock
import json, os

class AdminManager:
    _instance: Optional["AdminManager"] = None
    
    def __new__(cls) -> "AdminManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            print("[AdminManager] Creating new instance")
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "initialized"):
            return
        
        database = os.path.dirname(os.path.abspath(__file__))
        self.admins_db = os.path.join(database, "data", "admins.json")

        self.lock = RLock()
        self.bank = self.load()
        self.initialized = True

    def load(self) -> List[str]:
        with self.lock:
            try:
                with open(self.admins_db, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                return []
    
    def save(self, admins: List[str]) -> None:
        with self.lock:
            with open(self.admins_db, "w", encoding="utf-8") as f:
                json.dump(admins, f, indent=2)

    def add(self, admins: Union[List[str], str]) -> None:
        data = self.load()

        if isinstance(admins, list): data.extend(admins)
        elif isinstance(admins, str): data.append(admins)
        else: return

        self.save(list(dict.fromkeys(data)))

    def delete(self, admin: str) -> None:
        admins = self.load()
        admins.remove(admin)
        self.save(admins)

    def get_all(self) -> List[str]:
        return self.load()
    
    def __enter__(self) -> "AdminManager":
        self.lock.acquire()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.lock.release()