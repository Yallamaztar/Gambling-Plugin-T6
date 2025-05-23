import os, json
from typing import Dict, List, Optional

class Bank:
    def __init__(self, filepath: Optional[str] = None) -> None:
        if filepath is None:
            core = os.path.dirname(os.path.abspath(__file__))
            root = os.path.dirname(core)
            self.filepath = os.path.join(root, "bank_db.json")
        self.bank = self.load_bank()

    def load_bank(self) -> Dict:
        try:
            with open(self.filepath, 'r') as bank_file:
                return json.load(bank_file)
        except json.JSONDecodeError:
            return {}

    def save_bank(self) -> None:
        with open(self.filepath, 'w') as bank_file:
            json.dump(self.bank, bank_file, indent=2)

    def get_balance(self, player: str) -> int:
        balance = self.bank.get(player, 0)
        return balance

    def deposit(self, player: str, amount: int) -> None:
        self.bank[player] = self.get_balance(player) + amount
        self.save_bank()

    def get_top_balances(self, count: int = 5) -> List[Dict[str, int]]:
        top_players = sorted(self.load_bank().items(), key=lambda item: item[1], reverse=True)
        return [{"name": player, "balance": balance} for player, balance in top_players[:count]]