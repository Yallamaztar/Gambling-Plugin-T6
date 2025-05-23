from threading import Thread
from iw4m import IW4MWrapper
import time

from core.db import Bank

class GamblingManager:
    def __init__(self, server: IW4MWrapper.Server, commands: IW4MWrapper.Commands) -> None:
        self.bank     = Bank()
        self.server   = server
        self.commands = commands
        
        Thread(target=self.passive_income, daemon=True).start()
        Thread(target=self.broadcast_richest_players, daemon=True).start()

    def passive_income(self, amount: int = 1000000) -> None:
        while True:
            players = self.server.get_players()
            if len(players) == 0: time.sleep(10); continue
            
            for player in players:
                name = player['name']
                self.bank.deposit(player, amount)
                self.commands.privatemessage(name, f"You ^2received^7 ${amount}")

            time.sleep(300)

    def broadcast_richest_players(self) -> None:
        while True:
            top_players = self.bank.get_top_balances()
            self.commands.say("^7Top 5 ^5Richest^7 Players:")
            time.sleep(1)
            for i, player in enumerate(top_players):
                self.commands.say(f"^7#{i} {player['name']} - ^5{player['balance']}")
                
            time.sleep(600)