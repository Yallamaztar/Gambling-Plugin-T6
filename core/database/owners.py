from typing import List, Union
import json, os

class OwnerManager:
    def __init__(self):
        database = os.path.dirname(os.path.abspath(__file__))
        self.owners_db = os.path.join(database, "data", "owners.json")
        print("[OwnerManager] Database loaded")

    def load(self) -> List[str]:
        try:
            with open(self.owners_db, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save(self, owners: List[str]) -> None:
        with open(self.owners_db, 'w', encoding='utf-8' ) as f:
            json.dump(owners, f, indent=2)

    def add(self, owners: Union[List[str], str]) -> None:
        data = self.load()

        if isinstance(owners, list): data.extend(owners)
        elif isinstance(owners, str): data.append(owners)
        else: return

        self.save(list(dict.fromkeys(data)))

    def delete(self, owner: str) -> None:
        owners = self.load()
        owners.remove(owner)
        self.save(owners)

    def get_all(self) -> List[str]:
        return self.load()