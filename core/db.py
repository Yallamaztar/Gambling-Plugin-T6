import os, json
from typing import Dict, Optional

class Bank:
    def __init__(self, filepath: Optional[str] = None) -> None:
        if filepath is None:
            here = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(here)
            filepath = os.path.join(project_root, "bank_db.json")
        self.filepath = filepath
        self.bank = self.load_bank()

    def load_bank(self) -> Dict:
        try:
            with open(self.filepath, 'r') as bank_file:
                return json.load(bank_file)
        except json.JSONDecodeError:
            return {}

    def save_bank(self) -> None:
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, 'w') as bank_file:
            json.dump(self.bank, bank_file, indent=2)

    def get_balance(self, player: str) -> int:
        balance = self.bank.get(player, 0)
        return balance

    def deposit(self, player: str, amount: int) -> None:
        self.bank[player] = self.get_balance(player) + amount
        self.save_bank()
