import os
import subprocess
from . import immutable_os_config
from tools import immutable_installer
from rich.prompt import Prompt, Confirm

_user_account_group = [
    "wheel",
    "audio",
    "video",
    "storage",
    "network",
    "lp",
]

def run_openssl_passwd():
    # Tell the user what command is about to run
    print("\nThe system will now run: openssl passwd -6")
    print("Enter your password when prompted (it will ask twice to confirm).\n")

    # Run openssl passwd -6 and capture its output
    # capture_output=True means we grab stdout/stderr instead of printing them directly
    # text=True means the output is returned as a string instead of raw bytes
    result = subprocess.run(
        ["openssl", "passwd", "-6"],
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


def add_user():
    os.system("clear")

    # Get the users dictionary from config, create it if it does not exist yet
    users = immutable_os_config._config["accounts"].setdefault("users", {})

    print("\n-*- Add User -*-")

    # Keep asking until the user provides a valid, unique username
    while True:
        username = input("Username: ").strip()

        if not username:
            print("Username cannot be empty!")
        elif username in users:
            print("User already exists!")
        else:
            break

    # Keep running openssl until we successfully get a password hash
    while True:
        password_hash = run_openssl_passwd()

        if password_hash:
            # Show the resulting hash so the user can see what was stored
            print(f"\nPassword hash: {password_hash}")
            break
        else:
            print("Something went wrong, please try again...")

    # Let the user pick which groups this account should belong to
    print("\nAvailable groups:")
    print(" ".join(_user_account_group))
    raw = input("Groups (space separated): ").strip()

    groups = []
    invalid_groups = []

    if raw:
        for g in raw.split():
            if g in _user_account_group:
                groups.append(g)
            else:
                # Collect invalid group names to warn the user later
                invalid_groups.append(g)

        if invalid_groups:
            print(f"Warning: invalid groups ignored -> {' '.join(invalid_groups)}")

    # Save the new user into the config, storing the hash instead of a plain password
    users[username] = {
        "password": password_hash,
        "group": groups
    }

    print(f"\nUser '{username}' added successfully!")


def user_account_status():
    users = immutable_os_config._config["accounts"].get("users", {})

    lines = ["User accounts:"]

    for idx, (username, info) in enumerate(users.items(), start=1):
        # Show the stored hash directly, or "Not set" if there is none
        password_hash = info.get("password") or "Not set"

        raw_groups = info.get("group") or []

        # Separate valid and invalid groups for a cleaner status display
        valid = [g for g in raw_groups if g in _user_account_group]
        invalid = [g for g in raw_groups if g not in _user_account_group]

        group_display = ", ".join(valid) if valid else "Not set"

        if invalid:
            group_display += f" (invalid: {', '.join(invalid)})"

        lines.extend([
            "",
            f"{idx}. {username}",
            f"   Password hash: {password_hash}",
            f"   Groups: {group_display}",
        ])

    return "\n".join(lines)


def configure_user():
    os.system("clear")
    users = immutable_os_config._config["accounts"].get("users", {})

    if not users:
        print("No users available!")
        return

    print("\n-*- Configure User -*-")

    username = input("Enter username to configure: ").strip()

    if username not in users:
        print("User not found!")
        return

    while True:
        print(f"\n--- Editing: {username} ---")
        print("1. Rename user")
        print("2. Change password")
        print("3. Edit groups")
        print("4. Delete user")
        print("0. Back")

        choice = Prompt.ask("Select", choices=["1", "2", "3", "4", "0"])

        # Option 1: rename the account
        if choice == "1":
            confirm = Confirm.ask("Are you sure you want to rename this user?")
            if confirm:
                while True:
                    new_name = input("New username: ").strip()

                    if not new_name:
                        print("Cannot be empty!")
                    elif new_name in users:
                        print("User already exists!")
                    else:
                        break

                # Move the user data to the new key and remove the old one
                users[new_name] = users.pop(username)
                print(f"Renamed '{username}' -> '{new_name}'")

                # Update the local variable so the rest of the loop uses the new name
                username = new_name
            else:
                return

        # Option 2: generate a new password hash via openssl
        elif choice == "2":
            confirm = Confirm.ask("Are you sure you want to change the password?")
            if confirm:
                # Keep retrying if openssl fails for any reason
                while True:
                    password_hash = run_openssl_passwd()

                    if password_hash:
                        print(f"\nNew password hash: {password_hash}")
                        break
                    else:
                        print("Something went wrong, please try again...")

                # Overwrite the old hash with the new one
                users[username]["password"] = password_hash
                print("Password updated!")
            else:
                return

        # Option 3: replace the group list for this user
        elif choice == "3":
            confirm = Confirm.ask("Are you sure you want to change the groups?")
            if confirm:
                print("\nAvailable groups:")
                print(" ".join(_user_account_group))
                raw = input("Enter groups (space separated): ").strip()

                groups = []
                invalid = []

                if raw:
                    for g in raw.split():
                        if g in _user_account_group:
                            groups.append(g)
                        else:
                            invalid.append(g)

                    if invalid:
                        print(f"Warning: ignored -> {' '.join(invalid)}")

                users[username]["group"] = groups
                print("Groups updated!")
            else:
                return

        # Option 4: permanently remove this user account
        elif choice == "4":
            confirm = input(f"Delete '{username}'? (y/n): ").lower()
            if confirm == "y":
                confirm_again = Confirm.ask("Are you absolutely sure you want to remove this user account?")
                if confirm_again:
                    users.pop(username)
                    print("User deleted!")
                    # Break out of the loop because this user no longer exists
                    break
            else:
                print("Cancelled.")

        # Option 0: go back to the previous menu
        elif choice == "0":
            break