from core.commands import owners_only, run_command_threaded
from core.database.owners import OwnerManager
from core.wrapper import Wrapper

class OwnerAddCommand:
    def __init__(self, player: str, target: str) -> None:
        self.player = Wrapper().player
        self.manager = OwnerManager()
        self.add(player, target)
        return
    
    @owners_only()
    def add(self, player: str, target: str) -> None:
        self.manager.add(self.player.find_player_by_partial_name(target))

class OwnerRemoveCommand:
    def __init__(self, player: str, target: str) -> None:
        self.player = Wrapper().player
        self.manager = OwnerManager()
        self.remove(player, target)
        return

    @owners_only()
    def remove(self, player: str, target: str) -> None:
        self.manager.delete(target)

def add_owner(player: str, target: str) -> None:
    run_command_threaded(OwnerAddCommand, player, target)

def remove_owner(player: str, target: str) -> None:
    run_command_threaded(OwnerRemoveCommand, player, target)