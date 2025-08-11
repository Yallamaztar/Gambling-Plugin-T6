from concurrent.futures import ThreadPoolExecutor
from gsc_events import GSCClient
from core.database.bank import BankManager
from iw4m import IW4MWrapper

class EventManager:
    def __init__(self, bank: BankManager, commands: IW4MWrapper.Commands) -> None:
        self.client = GSCClient()
        self.client.delete_event_logs()

        self.bank = bank
        self.commands = commands

        executor = ThreadPoolExecutor(max_workers=5)

        self.register_events()
        executor.submit(self.client.run)
        print("[EventManager]: Running")

    def register_events(self) -> None:
        @self.client.on("player_connected")
        def on_connected(player: str) -> None:
            print(f"[EventManager]: {player} connected")
            self.bank.deposit(player, 200)
            self.commands.privatemessage(player, "Round Bonus: ^5$200")
        
        @self.client.on("player_killed")
        def on_killed(player: str, attacker: str, reason: str) -> None:
            print(f"[EventManager]: {player} killed by {attacker} - {reason}")
            self.bank.deposit(attacker, 400)
            self.commands.privatemessage(attacker, "Kill Bonus: ^5$400")
            