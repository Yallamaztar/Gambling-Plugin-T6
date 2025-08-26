from typing import Dict, Any
from concurrent.futures import ThreadPoolExecutor
from collections import deque
import time

from core.manager import GamblingManager
from core.registry import Register
from core.wrapper import Wrapper
from core.events import EventManager
from core.database.bank import BankManager
from core.bot import run_bot

class GamblingPlugin:
    def __init__(self) -> None:
        self.last_seen = set()
        
        wrapper = Wrapper()
        self.server = wrapper.server
        self.player = wrapper.player
        self.commands = wrapper.commands

        self.register = Register()
        self.executor = ThreadPoolExecutor(max_workers=12)

        bank = BankManager()
        # bank.reset()

        GamblingManager(bank, self.server, self.commands)
        EventManager(bank, self.commands)
        self.executor.submit(run_bot)

        print("[Gambling] Plugin running")
        self.run()
        
    def is_valid_audit_log(self, audit_log: Dict[str, Any]) -> bool:
        origin, data, log_time = audit_log['origin'], audit_log['data'], audit_log['time']
        return (origin, data, log_time) not in self.last_seen and origin != self.server.logged_in_as()

    def handle_command(self, origin: str, data: str) -> None:
        parts = data.strip().split()
        if not parts: return

        command = parts[0].lower()
        
        for registered_command, alias, callback in self.register._handlers:
            if command == registered_command or command == alias:
                args = [origin] + parts[1:]

                def run_callback():
                    try:
                        callback(*args)
                    except Exception:
                        self.commands.privatemessage(origin, "Do ^1!usage ^7to see ^3help ^7page")

                self.executor.submit(run_callback)
                break
                      
    def run(self) -> None:
        while True:
            audit_log = self.server.get_recent_audit_log()
            if audit_log is None or not self.is_valid_audit_log(audit_log):
                time.sleep(0.01)
                continue

            self.last_seen.add((audit_log['origin'], audit_log['data'], audit_log['time']))
            self.executor.submit(self.handle_command, audit_log['origin'], audit_log['data'])
            time.sleep(0.01)

if __name__ == '__main__':
    GamblingPlugin()