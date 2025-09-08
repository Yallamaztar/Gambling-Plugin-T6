from typing import Optional
from threading import RLock
import json, os

class TokenManager:
    _instance: Optional["TokenManager"] = None
    
    def __new__(cls) -> "TokenManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            print("[TokenManager] Creating new instance")
        return cls._instance
    
    def __init__(self) -> None:
        if hasattr(self, "initialized"):
            return
        
        database = os.path.dirname(os.path.abspath(__file__))
        self.tokens_db = os.path.join(database, "data", "tokens.json")

        self.lock = RLock()
        self.tokens = self.load()
        self.initialized = True

    def load(self) -> dict:
        with self.lock:
            try:
                with open(self.tokens_db, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                return {}

    def save(self, tokens: dict) -> None:
        with self.lock:
            with open(self.tokens_db, "w", encoding="utf-8") as f:
                json.dump(tokens, f, indent=2)

    def add(self, player: str, token: str) -> None:
        with self.lock:
            tokens = self.load()
            tokens[player] = token
            self.save(tokens)

    def delete(self, player: str) -> None:
        with self.lock:
            tokens = self.load()
            tokens.pop(player, None)
            self.save(tokens)

    def get_player_by_token(self, token: str) -> Optional[str]:
        with self.lock:
            tokens = self.load()
            for player, t in tokens.items():
                if t == token:
                    return player
            return
    
    def get_all(self) -> dict:
        with self.lock:
            return self.load()

    def __enter__(self) -> "TokenManager":
        self.lock.acquire()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.lock.release()
