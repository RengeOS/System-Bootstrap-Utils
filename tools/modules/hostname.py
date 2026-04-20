import re
import os
from rich import print
from . import immutable_os_config
from tools import immutable_installer

def is_valid_hostname(hostname):
    # Check characters
    if not hostname or len(hostname) > 253:
        return False

    labels = hostname.split(".")
    pattern = re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?$')

    # If the character is incorrect, immediately return False to the function
    for label in labels:
        if not pattern.match(label):
            return False

    return True

def set_hostname():
    os.system("clear")
    print("-*- Set Hostname -*-\n")

    while True:
        name = input(f"Enter your hostname [{immutable_os_config._config["system"]["hostname"]}]: ").strip()

        if not name:
            break

        if is_valid_hostname(name):
            immutable_os_config._config["system"]["hostname"] = name
            print("\n[green bold]Hostname has been successfully set![/green bold]")
            os.system("sleep 1")
            break
        else:
            print("[red]Invalid hostname.[/red] Only a-z, 0-9, hyphen allowed!")