import getpass
import os
from rich import print
from tools import immutable_installer
from . import configuration_config

def set_root_password():
    os.system("clear")
    print("-*- Root Password -*-")
    while True:
        pwd1 = getpass.getpass("Enter root password: ")
        pwd2 = getpass.getpass("Confirm root password: ")

        # Check empty
        if not pwd1:
            print("Password cannot be empty!\n")
            continue

        # Check match
        if pwd1 != pwd2:
            print("Passwords do not match!\n")
            continue

        # Save
        configuration_config._config["root_password"] = pwd1
        print("\n[green bold]Root password has been successfully set![/green bold]")
        os.system("sleep 1")
        break