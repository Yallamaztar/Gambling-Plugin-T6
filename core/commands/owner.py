from core.commands import owners_only, run_command_threaded
from core.database.owners import OwnerManager
from core.wrapper import Wrapper

class OwnerAddCommand:
    def __init__(self, player: str, target: str) -> None:
        self.player   = Wrapper().player
        self.commands = Wrapper().commands
        self.manager  = OwnerManager()
        self.add(player, target)
    
    @owners_only()
    def add(self, player: str, target: str) -> None:
        target = self.player.find_player_by_partial_name(target) # type: ignore
        if not target:
            self.commands.privatemessage(player, f"Player {target} not found"); return
        
        self.manager.add(target)
        self.commands.privatemessage(player, f"Added {target} as an owner")

class OwnerRemoveCommand:
    def __init__(self, player: str, target: str) -> None:
        self.player   = Wrapper().player
        self.commands = Wrapper().commands
        self.manager = OwnerManager()
        self.remove(player, target)

    @owners_only()
    def remove(self, player: str, target: str) -> None:
        target = self.player.find_player_by_partial_name(target) # type: ignore
        if not target:
            self.commands.privatemessage(player, f"Player {target} not found"); return
        
        self.manager.delete(target)
        self.commands.privatemessage(player, f"Removed {target} from owners")

def add_owner(player: str, target: str) -> None:
    run_command_threaded(OwnerAddCommand, player, target)

def remove_owner(player: str, target: str) -> None:
    run_command_threaded(OwnerRemoveCommand, player, target)