from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict
from iw4m import IW4MWrapper
import time

from core.database.bank import BankManager

class GamblingManager:
    def __init__(self, bank: BankManager, server: IW4MWrapper.Server, commands: IW4MWrapper.Commands) -> None:
        self.bank     = bank
        self.server   = server
        self.commands = commands

        self.executor = ThreadPoolExecutor()
        self.executor.submit(self.passive_income)
        self.executor.submit(self.broadcast_hint)
        self.executor.submit(self.broadcast_socialmedia)
        print("[GamblingManager] Running")
    
    def passive_income(self, amount: int = 250_000) -> None:
        while True:
            players: List[Dict[str, str]] = self.server.get_players()
            if len(players) == 0: time.sleep(10); continue

            for player in players:
                self.bank.deposit(player['name'], amount)
                self.commands.privatemessage(player['name'], f"You ^2received^7 ${amount}")
            
            time.sleep(600)

    def broadcast_hint(self) -> None:
        hints = [
            "^7Need help? Type ^3!usage ^7or ^3!u ^7to see all gambling options",
            "^7!banflip may get you temp banned with no unban",
            "^7Check your balance anytime with ^3!bal",
            "^7Found a ^1bug? ^3Report ^7it instead of abusing it and get paid ^F:^1100^7:",
            "^7Join our Discord for updates & events: ^5dsc.gg/browner",
        ]
        while True:
            time.sleep(160)
            for hint in hints:
                self.commands.say(hint); time.sleep(160)

    def broadcast_socialmedia(self) -> None:
        time.sleep(450)
        self.commands.say("^7Follow Our Social ^5Medias"); time.sleep(.25)
        self.commands.say("^7you^1tube^7.com/@^5BrowniesSnD"); time.sleep(.25)
        self.commands.say("^0x^7.com/^5BrowniesSnD"); time.sleep(.25)
