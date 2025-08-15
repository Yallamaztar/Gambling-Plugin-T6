from core.wrapper import Wrapper
from core.commands import run_command_threaded, rate_limit

import os
import json
import string, secrets

class LinkCommand:
    def __init__(self, player: str) -> None:
        commands  = os.path.dirname(os.path.abspath(__file__))
        tokens_db = os.path.join(commands, "..", "database", "data", "tokens.json")
        
        token = self.generate_token()
        self.save_token(player, token, path=tokens_db)
        Wrapper().commands.privatemessage(player, f"Your token: {token}")
        Wrapper().commands.privatemessage(player, f"Now go to our discord server and type /link <token>")
        print(f"[LinkCommand] {player} - {token}")

    def generate_token(self) -> str:
        chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(chars) for _ in range(5))
    
    def save_token(self, player: str, token: str, *, path: str) -> None:
        with open(path, "r") as f:
            try: tokens = json.load(f)
            except json.JSONDecodeError: tokens = {}

        tokens[player] = token

        with open(path, "w") as f:
            json.dump(tokens, f, indent=4)

        return

@rate_limit(minutes=3)
def link(player: str) -> None:
    run_command_threaded(LinkCommand, player)