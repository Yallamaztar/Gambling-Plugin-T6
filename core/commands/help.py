from core.wrapper import Wrapper
from core.commands import run_command_threaded, rate_limit
from typing import Optional

class HelpCommand:
    def __init__(self, player: str, command: Optional[str] = None) -> None:
        self.commands = Wrapper().commands

        if command is None:
            self.commands.privatemessage(player, "^7-- ^5Available Commands ^7--")
            self.commands.privatemessage(player, "^7Use ^3!help ^7<command> for detailed info on any command")
            self.commands.privatemessage(player, "^7Example: ^3!help gamble ^7for gambling commands")
        
        else:
            self.show_help(player, command)

    def show_help(self, player: str, command: str) -> None:
        help = {
            # Basic Commands
            "gamble": [
                "^7-- ^5Gamble Command Help ^7--",
                "^7Usage: ^5!gamble ^7<amount>",
                "^7Description: Gamble your money with a ^550^7/^150 chance to win or lose",
                "^7Example: ^5!gamble 10m"
            ],
            "balance": [
                "^7-- ^5Balance Command Help ^7--",
                "^7Usage: ^5!balance ^7[<player>]",
                "^7Description: Check your or another player's balance",
                "^7Example: ^5!balance",
                "^7Example: ^5!balance <player>"
            ],
            "pay": [
                "^7-- ^5Pay Command Help ^7--",
                "^7Usage: ^5!pay ^7<player> <amount>",
                "^7Description: Send money to another player",
                "^7Example: ^5!pay <player> 5k"
            ],
            #Shop
            "shop": [
                "^7-- ^5Shop Command Help ^7--",
                "^7Usage: ^5!shop ^7[<item_number>]",
                "^7Description: Open the shop menu or purchase an item",
                "^7Example: ^5!shop",
                "^7Example: ^5!shop ^71"
            ],
            # Help
            "help": [
                "^7-- ^5Help Command Help ^7--",
                "^7Usage: ^5!help ^7[<command>]",
                "^7Description: Get help information for a specific command",
                "^7Example: ^5!help gamble",
                "^7Example: ^5!help balance"
            ],
            # Claimables
            "hourly": [
                "^7-- ^5Hourly Claim Help ^7--",
                "^7Usage: ^5!hourly",
                "^7Description: Claim ^55,000 ^7every hour (1h cooldown)",
                "^7Example: ^5!hourly"
            ],
            "daily": [
                "^7-- ^5Daily Claim Help ^7--",
                "^7Usage: ^5!daily",
                "^7Description: Claim ^550,000 ^7every 24 hours (24h cooldown)",
                "^7Example: ^5!daily"
            ],
            "weekly": [
                "^7-- ^5Weekly Claim Help ^7--",
                "^7Usage: ^5!weekly",
                "^7Description: Claim ^5450,000 ^7every 7 days (7d cooldown)",
                "^7Example: ^5!weekly"
            ],
            "monthly": [
                "^7-- ^5Monthly Claim Help ^7--",
                "^7Usage: ^5!monthly",
                "^7Description: Claim ^54,000,000 ^7every 30 days (30d cooldown)",
                "^7Example: ^5!monthly"
            ],
            # Usage
            "usage": [
                "^7-- ^5Usage Command Help ^7--",
                "^7Usage: ^5!usage ^7[<page_number>]",
                "^7Description: View pages of usage instructions and tips",
                "^7Example: ^5!usage",
                "^7Example: ^5!usage 2",
                "^7Pages:",
                "  ^51^7: Basic commands like gamble, balance, pay",
                "  ^52^7: Daily claim commands and cooldowns",
                "  ^53^7: Shop commands and purchasing",
                "  ^54^7: Other useful tips and tricks"
            ]
        }

        if command.lower() in help:
            for line in help[command]: 
                self.commands.privatemessage(player, line)
        else:
            self.commands.privatemessage(player, f"^7No help available for ^5{command}")

@rate_limit(seconds=15)
def help(player: str, command: str) -> None:
    run_command_threaded(HelpCommand, player, command)