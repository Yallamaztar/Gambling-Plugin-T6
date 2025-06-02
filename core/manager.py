from threading import Thread
from iw4m import IW4MWrapper
import time

from core.database.bank import BankManager

class GamblingManager:
    def __init__(self, server: IW4MWrapper.Server, commands: IW4MWrapper.Commands) -> None:
        self.bank     = BankManager()
        self.server   = server
        self.commands = commands

        Thread(target=self.passive_income, daemon=True).start()
        Thread(target=self.broadcast_richest_players, daemon=True).start()
        Thread(target=self.broadcast_hint, daemon=True).start()

    def passive_income(self, amount: int = 10000000) -> None:
        while True:
            players = self.server.get_players()
            if len(players) == 0: time.sleep(10); continue

            for player in players:
                self.bank.deposit(player['name'], amount)
                self.commands.privatemessage(player['name'], f"You ^2received^7 ${amount}")
            
            time.sleep(1100)

    def broadcast_richest_players(self) -> None:
        while True:
            time.sleep(500)
            top_players = self.bank.top_balances()
            self.commands.say("^7Top 5 ^5Richest^7 Players:")

            time.sleep(.5)
            for i, player in enumerate(top_players):
                self.commands.say(f"^7#{i + 1} {player['name']} - ^5{player['balance']}")
                time.sleep(.2)

    def broadcast_hint(self) -> None:
        while True:
            time.sleep(225)
            self.commands.say("^7Need help? Type ^3!usage ^7or ^3!u ^7to see all gambling options")