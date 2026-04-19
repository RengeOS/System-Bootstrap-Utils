import getpass
import os
from tools import immutable_installer
from . import configuration_config

def set_root_password():
    os.system("clear")
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
        print("Root password set successfully!")
        os.system("sleep 1")
        break