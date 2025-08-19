from concurrent.futures import ThreadPoolExecutor
from gsc_events import GSCClient
from core.database.bank import BankManager
from iw4m import IW4MWrapper
import os

class EventManager:
    def __init__(self, bank: BankManager, commands: IW4MWrapper.Commands) -> None:
        self.client = GSCClient()
        self.client.clear_events()

        self.bank = bank
        self.commands = commands

        executor = ThreadPoolExecutor()

        self.register_events()
        executor.submit(self.client.run)
        print("[EventManager]: Running")

    def register_events(self) -> None:
        @self.client.on("player_spawned")
        def on_connected(player: str) -> None:
            self.bank.deposit(player, 2500)
            self.commands.privatemessage(player, "Spawn Bonus: ^5$2500")
        
        @self.client.on("player_killed")
        def on_killed(player: str, attacker: str, reason: str, weapon: str, hit_loc: str) -> None:
            if player == attacker: # suicide
                self.bank.deposit(player, 25000)
                self.commands.privatemessage(player, "Suicide Bonus: ^5$25,000")
            else:
                self.bank.deposit(attacker, 15000)
                self.commands.privatemessage(attacker, "Kill Bonus: ^5$15,000")