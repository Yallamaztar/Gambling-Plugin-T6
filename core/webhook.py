import requests
from datetime import datetime, timezone
from os import environ

def current_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()

def send_webhook(data: dict[str, list) -> None:
    try: requests.post(environ["DISCORD_WEBHOOK"], json=data, timeout=5)
    except Exception: return

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
    send_webhook(data)

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
    send_webhook(data)

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
    send_webhook(data)

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
    send_webhook(data)

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
    send_webhook(data)

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
    send_webhook(data)
