import requests
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from os import environ

# lightweight pool to avoid blocking command threads on network
_webhook_executor = ThreadPoolExecutor(max_workers=4)

def _submit_post(url: str, data: dict) -> None:
    def _run() -> None:
        try:
            requests.post(url, json=data, timeout=3)
        except Exception:
            # swallow webhook errors; we don't want to impact gameplay
            pass
    _webhook_executor.submit(_run)

def current_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()

def win_webhook(player: str, amount: str) -> None:
    data = {
        "embeds": [{
            "title": "Gamble Win 🎉",
            "avatar_url": "https://github.com/Yallamaztar/Gambling-Plugin-T6/blob/main/assets/gambla_win.png?raw=true",
            "description": f"**{player}** won **${amount}**",
            "color": 0x00ff00,
            "timestamp": current_timestamp()
        }]
    }
    _submit_post(environ["DISCORD_WIN_WEBHOOK"], data)

def loss_webhook(player: str, amount: str) -> None:
    data = {
        "embeds": [{
            "title": "Gamble Loss 😿",
            "avatar_url": "https://github.com/Yallamaztar/Gambling-Plugin-T6/blob/main/assets/gambla_loss.png?raw=true",
            "description": f"**{player}** lost **${amount}**",
            "color": 0xff0000,
            "timestamp": current_timestamp()
        }]
    }
    _submit_post(environ["DISCORD_LOSS_WEBHOOK"], data)

def link_webhook(player: str, discord_id: str) -> None:
    data = {
        "embeds": [{
            "title": "Account Linked 🔗",
            "avatar_url": "https://github.com/Yallamaztar/Gambling-Plugin-T6/blob/main/assets/gambla_no_avatar.png?raw=true",
            "description": f"Player **{player}** has linked their account to Discord <@{discord_id}>",
            "color": 0x3498db,
            "timestamp": current_timestamp()
        }]
    }
    _submit_post(environ["DISCORD_LINK_WEBHOOK"], data)

def unban_webhook(player: str, unbanned: str) -> None:
    data = {
        "embeds": [{
            "title": "Player Unbanned ✅",
            "avatar_url": "https://github.com/Yallamaztar/Gambling-Plugin-T6/blob/main/assets/gambla_no_avatar.png?raw=true",
            "description": f"Player **{unbanned}** has been unbanned by **{player}**",
            "color": 0x2ecc71,
            "timestamp": current_timestamp()
        }]
    }
    _submit_post(environ["DISCORD_UNBAN_WEBHOOK"], data)

def banflip_win_webhook(player: str, amount: str, duration: str) -> None:
    data = {
        "embeds": [{
            "title": "Banflip Win 🔥",
            "avatar_url": "https://github.com/Yallamaztar/Gambling-Plugin-T6/blob/main/assets/banflip_win.png?raw=true",
            "description": (
                f"**{player}** won a banflip with duration **duration {duration}!**\n"
                f"**Winnings:** ${amount}\n"
            ),
            "color": 0x1abc9c,
            "timestamp": current_timestamp()
        }]
    }
    _submit_post(environ["DISCORD_BANFLIP_WIN_WEBHOOK"], data)

def banflip_loss_webhook(player: str, amount: str, duration: str) -> None:
    data = {
        "embeds": [{
            "title": "Banflip Loss 💀",
            "avatar_url": "https://github.com/Yallamaztar/Gambling-Plugin-T6/blob/main/assets/banflip_loss.png?raw=true",
            "description": (
                f"**{player}** lost a banflip with **duration {duration}!**\n"
                f"**Lost Amount:** ${amount}\n"
            ),
            "color": 0xe74c3c,
            "timestamp": current_timestamp()
        }]
    }
    _submit_post(environ["DISCORD_BANFLIP_LOSS_WEBHOOK"], data)