import requests
from datetime import datetime, timezone
from os import environ

def current_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()

def win_webhook(player: str, amount: str) -> None:
    data = {
        "embeds": [{
            "title": "Gamble Win 🎉",
            "description": f"**{player}** won **${amount}**",
            "color": 0x00ff00,
            "timestamp": current_timestamp()
        }]
    }
    requests.post(environ["DISCORD_WIN_WEBHOOK"], json=data, timeout=5)

def loss_webhook(player: str, amount: str) -> None:
    data = {
        "embeds": [{
            "title": "Gamble Loss 😿",
            "description": f"**{player}** lost **${amount}**",
            "color": 0xff0000,
            "timestamp": current_timestamp()
        }]
    }
    requests.post(environ["DISCORD_LOSS_WEBHOOK"], json=data, timeout=5)

def link_webhook(player: str, discord_id: str) -> None:
    data = {
        "embeds": [{
            "title": "Account Linked 🔗",
            "description": f"Player **{player}** has linked their account to Discord <@{discord_id}>",
            "color": 0x3498db,
            "timestamp": current_timestamp()
        }]
    }
    requests.post(environ["DISCORD_LINK_WEBHOOK"], json=data, timeout=5)

def unban_webhook(player: str, unbanned: str) -> None:
    data = {
        "embeds": [{
            "title": "Player Unbanned ✅",
            "description": f"Player **{unbanned}** has been unbanned by **{player}**",
            "color": 0x2ecc71,
            "timestamp": current_timestamp()
        }]
    }
    requests.post(environ["DISCORD_UNBAN_WEBHOOK"], json=data, timeout=5)