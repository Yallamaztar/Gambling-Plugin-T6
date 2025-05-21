import os, time
from iw4m import IW4MWrapper
from core.db import Bank
from core.registry import Register
from core.utils import printdebug, printinfo, printerror, banner

from typing import Dict, Any

class GamblingPlugin:
    def __init__(self) -> None:
        self.owner     = '[ACOG]budiwrld'
        self.last_seen = set()
        self.bank      = Bank()

        self.iw4m = IW4MWrapper(
            base_url  = os.environ['IW4M_URL'],
            server_id = os.environ['IW4M_ID'],
            cookie    = os.environ['IW4M_HEADER']
        )

        self.server   = self.iw4m.Server(self.iw4m)
        self.commands = self.iw4m.Commands(self.iw4m)
        self.register = Register(self.bank, self.commands)
        
        print(banner())

    def is_valid_audit_log(self, audit_log: Dict[str, Any]) -> bool:
        origin, log_time = audit_log['origin'], audit_log['time']
        return (origin, log_time) not in self.last_seen and origin != 'TonyBot'

    def handle_command(self, origin: str, data: str, time: str) -> None:
        parts = data.strip().split()
        if not parts:
            return
        
        command = parts[0]
        printdebug(f"Received command: {data} from {origin} - {time}")
        
        if command == "!give": 
            if origin == self.owner:
                try:
                    target, amount = parts[1], int(amount)
                    self.bank.deposit(target, int(amount))
                    self.commands.privatemessage(target, f"you have been ^2paid^7: ${amount}")
                    self.commands.privatemessage(origin, f"^2successfully^7 paid {target} ${amount}")
                    printinfo(f"{origin} gave ${amount} to {target}")
                except Exception:
                    printerror(f"Failed !give command | Most likely player not found")    
            else:
                self.commands.privatemessage(origin, "you dont have ^1perms^7 for this")
                printdebug(f"{origin} tried to use !give without permission")
        
        for registered_command, callback in self.register._handlers:
            if data.startswith(registered_command):
                try:
                    args = [origin] + parts[1:]
                    response = callback(*args)
                    if response:
                        player, message = response
                        self.commands.privatemessage(player, message)
                        printdebug(f"Executed {registered_command} for {origin}")
                except Exception:
                    printerror(f"Command error ({registered_command})")

    def run(self) -> None:
        printinfo("GamblingPlugin is now running.")
        while True:
            audit_log = self.server.get_recent_audit_log()
            if not self.is_valid_audit_log(audit_log):
                time.sleep(.1)
                continue

            origin = audit_log['origin']
            data   = audit_log['data']
            _time  = audit_log['time']
            self.last_seen.add((origin, _time))

            self.handle_command(origin, data, _time)
            time.sleep(.1)

if __name__ == '__main__':
    GamblingPlugin().run()