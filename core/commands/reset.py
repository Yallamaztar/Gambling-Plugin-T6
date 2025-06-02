from core.database.bank import BankManager
from core.commands import owners_only, run_command_threaded
from core.wrapper import Wrapper

class ResetCommand:
    def __init__(self, player: str) -> None:
        self.reset(player)

    @owners_only()
    def reset(self, player : str) -> None:
        BankManager().reset()
        Wrapper().commands.say(player, "^7Bank has been ^1reset")

def reset(player: str) -> None:
    run_command_threaded(ResetCommand, player)