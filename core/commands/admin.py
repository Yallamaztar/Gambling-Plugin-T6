from core.commands import run_command_threaded
from core.permissions import owners_only
from core.database.admins import AdminManager
from core.database.links import LinkManager
from core.wrapper import Wrapper

class AdminAddCommand:
    def __init__(self, player: str, target: str) -> None:
        self.player   = Wrapper().player
        self.commands = Wrapper().commands
        self.manager  = AdminManager()
        self.add(player, target)
    
    @owners_only()
    def add(self, player: str, target: str) -> None:
        target = LinkManager().find_linked_by_partial_name(target)
        if not target:
            self.commands.privatemessage(player, f"Player {target} not found"); return
        
        self.manager.add(target)
        self.commands.privatemessage(player, f"Added {target} as an owner")

class AdminRemoveCommand:
    def __init__(self, player: str, target: str) -> None:
        self.player   = Wrapper().player
        self.commands = Wrapper().commands
        self.manager = AdminManager()
        self.remove(player, target)

    @owners_only()
    def remove(self, player: str, target: str) -> None:
        target = LinkManager().find_linked_by_partial_name(target)
        if not target:
            self.commands.privatemessage(player, f"Player {target} not found"); return
        
        self.manager.delete(target)
        self.commands.privatemessage(player, f"Removed {target} from owners")

def add_admin(player: str, target: str) -> None:
    run_command_threaded(AdminAddCommand, player, target)

def remove_admin(player: str, target: str) -> None:
    run_command_threaded(AdminRemoveCommand, player, target)