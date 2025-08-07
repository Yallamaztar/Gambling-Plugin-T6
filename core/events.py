from gsc_events import GSCClient
from core.database.bank import BankManager
from core.wrapper import Wrapper
from typing import Dict, Any
import random

class EventManager:
    def __init__(self) -> None:
        self.client = GSCClient()
        self.bank = BankManager()
        self.commands = Wrapper().commands

        self.events()
        self.client.run()

    def events(self) -> None:
        @self.client.on("player_connected")
        def on_connected(player: str) -> None:
            self.bank.deposit(player, 1000)
            self.commands.privatemessage(player, "You received a ^2$1000^7 connection bonus!")
            return 
        
        @self.client.on("player_killed")
        def on_killed(player: str, attacker: str, reason: str) -> None:
            print("Killed: " + player)
            self.bank.deposit(attacker, 5000)
            self.commands.privatemessage(attacker, f"Kill reward: ^2$5000")
            return

        return