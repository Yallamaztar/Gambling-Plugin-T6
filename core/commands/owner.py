from core.commands import owners_only, run_command_threaded
from core.database.owners import OwnerManager
from core.wrapper import Wrapper

class OwnerCommand:
    def __init__(self, player: str) -> None:
        self.player = Wrapper().player
        self.manager = OwnerManager()

    @owners_only()
    def add(self, player: str, target: str) -> None:
        self.manager.add(self.player.find_player_by_partial_name(target))

    @owners_only()
    def remove(self, player: str, target: str) -> None:
        self.manager.delete(target)