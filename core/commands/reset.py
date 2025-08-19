from core.database.bank import BankManager
from core.permissions import owners_only
from core.commands import run_command_threaded
from core.wrapper import Wrapper

class ResetCommand:
    def __init__(self, player: str) -> None:
        self.reset(player)

    @owners_only()
    def reset(self, player : str) -> None:
        BankManager().reset()
        Wrapper().commands.say("^7Bank has been ^1reset")

def reset(player: str) -> None:
    run_command_threaded(ResetCommand, player)