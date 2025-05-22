import os, time
from iw4m import IW4MWrapper
from core.db import Bank
from core.registry import Register
from core.utils import banner

from typing import Dict, Any
from threading import Thread


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
        self.player   = self.iw4m.Player(self.iw4m)
        self.commands = self.iw4m.Commands(self.iw4m)

        self.register = Register(self.owner,
            bank     = self.bank,
            server   = self.server,
            commands = self.commands,
            player   = self.player
        )

        print(banner())

    def is_valid_audit_log(self, audit_log: Dict[str, Any]) -> bool:
        origin, log_time = audit_log['origin'], audit_log['time']
        return (origin, log_time) not in self.last_seen and origin != 'TonyBot'

    def handle_command(self, origin: str, data: str, time: str) -> None:
        parts = data.strip().split()
        if not parts:
            return

        for registered_command, callback in self.register._handlers:
            if data.startswith(registered_command):
                args = [origin] + parts[1:]

                def run_callback():
                    try:
                        callback(*args)
                    except Exception:
                        if origin != self.owner:
                            self.commands.kick(origin, "fuck you nigga")

                Thread(target=run_callback).start()

    def run(self) -> None:
        while True:
            audit_log = self.server.get_recent_audit_log()
            if not self.is_valid_audit_log(audit_log):
                time.sleep(.1)
                continue

            origin = audit_log['origin']
            data   = audit_log['data']
            _time  = audit_log['time']
            
            self.last_seen.clear()
            self.last_seen.add((origin, _time))

            self.handle_command(origin, data, _time)
            time.sleep(.1)

if __name__ == '__main__':
    GamblingPlugin().run()
