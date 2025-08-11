from concurrent.futures import ThreadPoolExecutor
from iw4m import IW4MWrapper
import time

from core.database.bank import BankManager

class GamblingManager:
    def __init__(self, bank: BankManager, server: IW4MWrapper.Server, commands: IW4MWrapper.Commands) -> None:
        self.bank     = bank
        self.server   = server
        self.commands = commands

        self.executor = ThreadPoolExecutor(max_workers=2)
        self.executor.submit(self.passive_income)
        self.executor.submit(self.broadcast_hint)
    
    def passive_income(self, amount: int = 250_000) -> None:
        while True:
            players = self.server.get_players()
            if len(players) == 0: time.sleep(10); continue

            for player in players:
                self.bank.deposit(player['name'], amount)
                self.commands.privatemessage(player['name'], f"You ^2received^7 ${amount}")
            
            print(f"[GamblingManager]: Ran `passive_income` for {len(players)} players")
            time.sleep(600)

    def broadcast_hint(self) -> None:
        while True:
            time.sleep(450)
            self.commands.say("^7Need help? Type ^3!usage ^7or ^3!u ^7to see all gambling options")
            print(f"[GamblingManager]: Ran `broadcast_hint`")
