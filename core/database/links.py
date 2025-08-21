from typing import Optional
from threading import RLock
import json, os

class LinkManager:
    _instance: Optional["LinkManager"] = None

    def __new__(cls) -> "LinkManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            print("[LinkManager] Creating new instance")
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "initialized"):
            return

        database = os.path.dirname(os.path.abspath(__file__))
        self.links_db = os.path.join(database, "data", "linked.json")

        self.lock = RLock()
        self.links = self.load()
        self.initialized = True

    def load(self) -> dict:
        with self.lock:
            try:
                with open(self.links_db, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                return {}

    def save(self, links: dict) -> None:
        with self.lock:
            with open(self.links_db, "w", encoding="utf-8") as f:
                json.dump(links, f, indent=2)

    def link_account(self, discord_id: int, player: str) -> None:
        links = self.load()
        links[str(discord_id)] = player
        self.save(links)

    def unlink_account(self, discord_id: int) -> None:
        links = self.load()
        links.pop(str(discord_id), None)
        self.save(links)

    def get_player_by_discord(self, discord_id: int) -> Optional[str]:
        links = self.load()
        return links.get(str(discord_id))

    def is_linked(self, player: str) -> bool:
        links = self.load()
        return player in links.values()

    def get_all(self) -> dict:
        return self.load()

    def find_linked_by_partial_name(self, player: str) -> str: # type: ignore
        player = player.lower()
        links  = self.get_all()

        for discord_id, linked in links.items():
            if player in linked.lower():
                return linked

    def __enter__(self) -> "LinkManager":
        self.lock.acquire()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.lock.release()