from core.wrapper import Wrapper
from core.commands import run_command_threaded, rate_limit
from core.database.links import LinkManager
from core.database.tokens import TokenManager
from core.permissions import admins_only

import string, secrets

class LinkCommand:
    def __init__(self, player: str) -> None:
        self.player = player
        self.token = self.generate_token()
        self.save_token()
        Wrapper().commands.privatemessage(self.player, f"Your token: {self.token}")
        Wrapper().commands.privatemessage(
            self.player, "Now go to our Discord server and type /link <token>"
        )
        print(f"[LinkCommand] {player} - {self.token}")

    def generate_token(self) -> str:
        chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(chars) for _ in range(5))
    
    def save_token(self) -> None:
        TokenManager().add(self.player, self.token)

class IsLinkedCommand:
    def __init__(self, player: str, target: str) -> None:
        if not LinkManager().is_linked(target):
            Wrapper().commands.privatemessage(player, f"{target} has not linked theyre account yet")

@rate_limit(minutes=1)
def link(player: str) -> None:
    if LinkManager().is_linked(player):
        Wrapper().commands.privatemessage(player, "Your account is already linked"); return
    run_command_threaded(LinkCommand, player)

@admins_only()
def is_linked(player: str, target: str) -> None:
    run_command_threaded(IsLinkedCommand, player, target)