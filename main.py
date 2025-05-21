import os, time
from iw4m import IW4MWrapper
from core.db import Bank
from core.registry import Register

from typing import Dict, Any

class GamblingPlugin:
    def __init__(self) -> None:
        self.owner     = '[ACOG]budiwrld'
        self.last_seen = set()
        self.bank      = Bank()
        self.register  = Register(self.bank)

        self.iw4m = IW4MWrapper(
            base_url  = os.environ['IW4M_URL'],
            server_id = os.environ['IW4M_ID'],
            cookie    = os.environ['IW4M_HEADER']
        )

        self.server   = self.iw4m.Server(self.iw4m)
        self.commands = self.iw4m.Commands(self.iw4m)

    def is_valid_audit_log(self, audit_log: Dict[str, Any]) -> bool:
        origin, log_time = audit_log['origin'], audit_log['time']
        return (origin, log_time) not in self.last_seen and origin != 'TonyBot'

    def handle_command(self, origin: str, data: str) -> None:
        parts = data.strip().split()
        if not parts:
            return
        
        command = parts[0]
        
        if command == "!pay" and origin == self.owner:
            self.bank.deposit(parts[1], int(parts[2]))
            self.commands.privatemessage(parts[1], f"you have been ^2paid^7: ${parts[2]}")
            self.commands.privatemessage(origin, f"^2successfully^7 paid {parts[1]} ${parts[2]}")
            
        if command == "!pay" and origin != self.owner:
            self.commands.privatemessage(origin, "you dont have ^1perms^7 for this")
        
        for registered_command, callback in self.register._handlers:
            if data.startswith(registered_command):
                try:
                    args = [origin] + parts[1:]
                    response = callback(*args)
                    if response:
                        player, message = response
                        self.commands.privatemessage(player, message)
                except Exception:
                    pass

    def run(self) -> None:
        while True:
            audit_log = self.server.get_recent_audit_log()
            if not self.is_valid_audit_log(audit_log):
                time.sleep(0.1)
                continue

            origin = audit_log['origin']
            data = audit_log['data']
            self.last_seen.add((origin, audit_log['time']))

            self.handle_command(origin, data)
            time.sleep(.1)

if __name__ == '__main__':
    GamblingPlugin().run()