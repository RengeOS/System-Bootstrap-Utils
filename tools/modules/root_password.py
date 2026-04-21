import os
import subprocess
from . import immutable_os_config


def run_openssl_passwd():
    result = subprocess.run(
        ["openssl", "passwd", "-6"], # For generation hash password
        capture_output=True,
        text=True
    )

    # If the command failed (non-zero exit code), show the error and return nothing
    if result.returncode != 0:
        print(f"Error running openssl: {result.stderr.strip()}")
        return None

    # Remove any leading/trailing whitespace or newline characters from the output
    password_hash = result.stdout.strip()

    # If the output is empty for some reason, treat it as a failure
    if not password_hash:
        print("Could not get hash from openssl!")
        return None

    return password_hash


def set_root_password():
    os.system("clear")

    print("-*- Root Password -*-")

    # Keep running openssl until we successfully get a password hash
    while True:
        password_hash = run_openssl_passwd()

        if password_hash:
            # Show the resulting hash so the user can see what was stored
            print(f"\nPassword hash: {password_hash}")
            break
        else:
            print("Something went wrong, please try again...")

    # Save the hash into the root account config
    immutable_os_config._config["accounts"]["root"]["password"] = password_hash

    print("\nRoot password has been successfully set!")
    os.system("sleep 1")