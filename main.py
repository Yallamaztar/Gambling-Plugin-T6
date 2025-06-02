from typing import Dict, Any, Set, Tuple
from threading import Thread
import time

from core.database.owners import OwnerManager
from core.manager import GamblingManager
from core.registry import Register
from core.wrapper import Wrapper

class GamblingPlugin:
    def __init__(self) -> None:
        self.last_seen: Set[Tuple[str, str, str]] = set()

        wrapper = Wrapper()
        self.server = wrapper.server
        self.player = wrapper.player
        self.commands = wrapper.commands

        self.register = Register(OwnerManager().load(),
            server   = self.server,
            commands = self.commands,
            player   = self.player
        )

        GamblingManager(self.server, self.commands)
        self.run()
    
    def is_valid_audit_log(self, audit_log: Dict[str, Any]) -> bool:
        origin, data, log_time = audit_log['origin'], audit_log['data'], audit_log['time']
        return (origin, data, log_time) not in self.last_seen and origin != self.server.logged_in_as()

    def handle_command(self, origin: str, data: str) -> None:
        parts = data.strip().split()
        if not parts:
            return

        for registered_command, alias, callback in self.register._handlers:
            if parts[0] == registered_command or parts[0] == alias:
                args = [origin] + parts[1:]

                def run_callback():
                    try:
                        callback(*args)
                    except Exception:
                        Wrapper().commands.kick(origin, "fuck you")

                Thread(target=run_callback).start()
                break
            
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
            self.last_seen.add((audit_log['origin'], audit_log['data'], audit_log['time']))
            self.handle_command(audit_log['origin'], audit_log['data'])

            time.sleep(.1)

if __name__ == '__main__':
    GamblingPlugin()
