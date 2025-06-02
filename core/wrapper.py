from iw4m import IW4MWrapper
import os

class Wrapper:
    def __init__(self) -> None:
        iw4m = IW4MWrapper(
            base_url  = os.environ['IW4M_URL'],
            server_id = os.environ['IW4M_ID'],
            cookie    = os.environ['IW4M_HEADER']
        )

        self.server   = iw4m.Server(iw4m)
        self.player   = iw4m.Player(iw4m)
        self.commands = iw4m.Commands(iw4m)