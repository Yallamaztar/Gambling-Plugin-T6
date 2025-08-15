from concurrent.futures import ThreadPoolExecutor
from gsc_events import GSCClient
from core.database.bank import BankManager
from iw4m import IW4MWrapper

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
            print(f"[EventManager]: {player} connected")
            self.bank.deposit(player, 1000)
            self.commands.privatemessage(player, "Spawn Bonus: ^5$1000")
        
        @self.client.on("player_killed")
        def on_killed(player: str, attacker: str, reason: str) -> None:
            print(f"[EventManager]: {player} killed by {attacker} - {reason}")
            self.bank.deposit(attacker, 10000)
            self.commands.privatemessage(attacker, "Kill Bonus: ^5$10,000")
            