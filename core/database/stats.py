from typing import Dict, Optional, Union, List
from threading import RLock
import json, os

class StatsManager:
    _instance: Optional["StatsManager"] = None

    def __new__(cls) -> "StatsManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            print("[StatsManager] Creating new instance")
        return cls._instance

    def __init__(self):
        if hasattr(self, "initialized"):
            return
        
        database = os.path.dirname(os.path.abspath(__file__))
        self.stats_db = os.path.join(database, "data", "stats.json")

        self.lock = RLock()
        self.stats = self.load()
        self.initialized = True

    def load(self) -> Dict[str, Dict]:
        with self.lock:
            try:
                with open(self.stats_db, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
            
    def save(self) -> None:
        with self.lock:
            with open(self.stats_db, "w", encoding="utf-8") as f:
                json.dump(self.stats, f, indent=2)

    def ensure(self, player: str) -> None:
        if player not in self.stats:
            self.stats[player] = {"wins": 0, "losses": 0, "net": 0}
            self.save()
            
    def win(self, player: str, amount: int) -> None:
        with self.lock:
            self.ensure(player)
            self.stats[player]["wins"] += 1
            self.stats[player]["net"]  += amount
            self.save()

    def loss(self, player: str, amount: int) -> None:
        with self.lock:
            self.ensure(player)
            self.stats[player]["losses"] += 1
            self.stats[player]["net"] -= amount
            self.save()

    def top_stats(self, count: Optional[int] = 5, by: str = "net") -> List[Dict[str, Union[str, int]]]:
        with self.lock:
            if by not in {"wins", "losses", "net"}: by = "net"

            with self.lock:
                return [
                    {"name": player, "wins": stats.get("wins", 0), "losses": stats.get("losses", 0), "net": stats.get("net", 0)}
                    for player, stats in sorted(self.stats.items(), key=lambda item: item[1].get(by, 0), reverse=True)[:count]
                ]