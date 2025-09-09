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
        def on_spawned(player: str) -> None:
            if self.bank.balance(player) > 1_000_000_000:
                connect = int(.000001 * self.bank.balance(player))
            else:
                connect = 2500
            self.bank.deposit(player, connect)
            self.commands.privatemessage(player, f"Spawn Bonus: ^5${connect}")
        
        @self.client.on("player_killed")
        def on_killed(player: str, attacker: str, reason: str, weapon: str, hit_loc: str) -> None:
            if self.bank.balance(attacker) > 1_000_000_000: kill = int(.000005 * self.bank.balance(attacker))
            elif player == attacker: kill = -50_000
            else: kill = 10_000
            
            if player == self.bank.top_balances()[0]['name']:
                self.commands.say(f"^5{attacker} ^7killed ^5MVP ^7{player}!")
                kill += max(25_000, int(.000002 * self.bank.balance(player)))

            self.bank.deposit(attacker, kill)
            self.commands.privatemessage(attacker, f"Kill Bonus: ^5${kill}")

        @self.client.on("player_death")
        def on_death(player: str) -> None:
            if self.bank.balance(player) > 1_000_000_000:
                death = int(.000002 * self.bank.balance(player))
            else:
                death = 10000 
            self.bank.deposit(player, -death)
            self.commands.privatemessage(player, f"Death Penalty: ${death}")

        @self.client.on("player_disconnected")
        def on_disconnect(player: str) -> None:
            if self.bank.balance(player) > 1_000_000_000:
                disconnect = int(.0000015 * self.bank.balance(player))
            else:
                disconnect = 25000
            self.bank.deposit(player, -disconnect)

        print("[EventManager] Registered all events")
