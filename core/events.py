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
        self.kill_streaks: Dict[str, int] = {}

        self.events()
        self.client.run()

    def events(self) -> None:
        @self.client.on("player_connected")
        def on_connected(player: str) -> None:
            self.bank.deposit(player, 1000)
            self.commands.privatemessage(player, "You received a ^2$1000^7 connection bonus!")

        @self.client.on("player_killed")
        def on_killed(player: str, attacker: str, reason: str) -> None:
            if player == attacker:
                penalty = 10000
                self.bank.deposit(player, -penalty)
                self.commands.privatemessage(player, f"^1Suicide penalty^7: -${penalty}")
                return

            self.kill_streaks[player] = 0
            self.kill_streaks[attacker] = self.kill_streaks.get(attacker, 0) + 1
            streak = self.kill_streaks[attacker]
            
            reward = 5000
            if streak >= 5:
                streak_bonus = reward * (streak // 5)
                reward += streak_bonus
                self.commands.say(f"^7{attacker} is on a ^2{streak} ^7killstreak! (^2+${streak_bonus}^7)")

            self.bank.deposit(attacker, reward)
            self.commands.privatemessage(attacker, f"Kill reward: ^2+${reward}")
