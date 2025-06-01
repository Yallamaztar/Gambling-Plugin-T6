from colorama import just_fix_windows_console
from iw4m import IW4MWrapper
from typing import Dict, Set, Any
from threading import Thread
import os, time

from core.manager import GamblingManager
from core.registry import Register

class GamblingPlugin:
    def __init__(self) -> None:
        self.owner     = '[ACOG]budiwrld'
        self.last_seen: Set[str, str] = set()

        self.iw4m = IW4MWrapper(
            base_url  = os.environ['IW4M_URL'],
            server_id = os.environ['IW4M_ID'],
            cookie    = os.environ['IW4M_HEADER']
        )

        self.server   = self.iw4m.Server(self.iw4m)
        self.player   = self.iw4m.Player(self.iw4m)
        self.commands = self.iw4m.Commands(self.iw4m)

        self.register = Register(self.owner,
            server   = self.server,
            commands = self.commands,
            player   = self.player
        )

        GamblingManager(self.server, self.commands)
        print(self.server.logged_in_as())
        # lil ascii art neva hurt nobody
        print(f"""
\x1b[38;2;0;140;255m .88888.                      dP       dP oo
\x1b[38;2;0;130;255md8'   `88                     88       88
\x1b[38;2;0;120;255m88        .d8888b. 88d8b.d8b. 88d888b. 88 dP 88d888b. .d8888b.
\x1b[38;2;0;110;255m88   YP88 88'  `88 88'`88'`88 88'  `88 88 88 88'  `88 88'  `88
\x1b[38;2;0;100;255mY8.   .88 88.  .88 88  88  88 88.  .88 88 88 88    88 88.  .88
\x1b[38;2;0;90;255m `88888'  `88888P8 dP  dP  dP 88Y8888' dP dP dP    dP `8888P88
\x1b[38;2;0;80;255mooooooooooooooooooooooooooooooooooooooooooooooooooooooo~~~~.88~
\x1b[38;2;0;70;255m                                                       d8888P\x1b[0m
 ──────────────────────────────────────────────────────────
    """
        )

    def is_valid_audit_log(self, audit_log: Dict[str, Any]) -> bool:
        origin, log_time = audit_log['origin'], audit_log['time']
        return (origin, log_time) not in self.last_seen and origin != "TonyBot"

    def handle_command(self, origin: str, data: str, time: str) -> None:
        parts = data.strip().split()
        if not parts:
            return

        for registered_command, alias, callback in self.register._handlers:
            if data.startswith(registered_command) or data.startswith(alias):
                args = [origin] + parts[1:]

                def run_callback():
                    try:
                        callback(*args)
                    except Exception:
                        pass

                Thread(target=run_callback).start()

    def run(self) -> None:
        while True:
            audit_log = self.server.get_recent_audit_log()

            if audit_log is None:
                time.sleep(.1)
                continue

            if not self.is_valid_audit_log(audit_log):
                time.sleep(.1)
                continue

            self.last_seen.clear()
            self.last_seen.add((audit_log['origin'], audit_log['time']))

            self.handle_command(
                audit_log['origin'], audit_log['data'], audit_log['time']
            )

            time.sleep(.1)

if __name__ == '__main__':
    just_fix_windows_console()
    GamblingPlugin().run()
