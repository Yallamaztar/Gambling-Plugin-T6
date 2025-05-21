from colorama import just_fix_windows_console
just_fix_windows_console()

RESET = "\x1b[0m"
BLUE = "\x1b[38;2;0;150;255m"
BRIGHT_YELLOW = "\x1b[38;2;255;165;0m"
RED = "\x1b[38;2;255;51;51m"

def printinfo(info: str) -> None: print(f"{BLUE}[INFO]{RESET}:  {info}")
def printdebug(debug: str) -> None: print(f"{BRIGHT_YELLOW}[DEBUG]{RESET}: {debug}")
def printerror(error: str) -> None: print(f"{RED}[ERROR]{RESET}: {error}")

def banner() -> str:
    return f"""
\x1b[38;2;0;140;255m .88888.                      dP       dP oo                   
\x1b[38;2;0;130;255md8'   `88                     88       88                      
\x1b[38;2;0;120;255m88        .d8888b. 88d8b.d8b. 88d888b. 88 dP 88d888b. .d8888b. 
\x1b[38;2;0;110;255m88   YP88 88'  `88 88'`88'`88 88'  `88 88 88 88'  `88 88'  `88 
\x1b[38;2;0;100;255mY8.   .88 88.  .88 88  88  88 88.  .88 88 88 88    88 88.  .88 
\x1b[38;2;0;90;255m `88888'  `88888P8 dP  dP  dP 88Y8888' dP dP dP    dP `8888P88 
\x1b[38;2;0;80;255mooooooooooooooooooooooooooooooooooooooooooooooooooooooo~~~~.88~
\x1b[38;2;0;70;255m                                                       d8888P{RESET}  
 ──────────────────────────────────────────────────────────   
    """

def parse_amount(amount: str) -> int:
    if amount[-1].lower() == 'k':
        return int(float(amount[:-1]) * 1000)
    elif amount[-1].lower() == 'm':
        return int(float(amount[:-1]) * 1000000)
    elif amount[-1].lower() == 'b':
        return int(float(amount[:-1]) * 1000000000)
    elif amount[-1].lower() == 't':
        return int(float(amount[:-1]) * 1000000000000)
    else:
        return int(amount)