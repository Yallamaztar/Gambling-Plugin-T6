from typing import Optional, List, Union
from threading import RLock
import json, os

class OwnerManager:
    _instance: Optional["OwnerManager"] = None
    
    def __new__(cls) -> "OwnerManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            print("[OwnerManager] Creating new instance")
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "initialized"):
            return
        
        database = os.path.dirname(os.path.abspath(__file__))
        self.owners_db = os.path.join(database, "data", "owners.json")
        
        self.lock = RLock()
        self.bank = self.load()
        self.initialized = True

    def load(self) -> List[str]:
        with self.lock:
            try:
                with open(self.owners_db, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                return []

    def save(self, owners: List[str]) -> None:
        with self.lock:
            with open(self.owners_db, "w", encoding="utf-8" ) as f:
                json.dump(owners, f, indent=2)

    def add(self, owners: Union[List[str], str]) -> None:
        with self.lock:
            data = self.load()

            if isinstance(owners, list): data.extend(owners)
            else: data.append(owners)

            self.save(list(dict.fromkeys(data)))

    def delete(self, owner: str) -> None:
        with self.lock:
            owners = self.load()
            owners.remove(owner)
            self.save(owners)

    def get_all(self) -> List[str]:
        with self.lock:
            return self.load()
    
    def __enter__(self) -> "OwnerManager":
        self.lock.acquire()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.lock.release()
