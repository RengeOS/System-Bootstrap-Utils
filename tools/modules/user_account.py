import os
from . import configuration_config
from tools import immutable_installer
from getpass import getpass
from rich import print
from rich.prompt import Prompt, Confirm

_user_account_group = [
    "wheel",
    "audio",
    "video",
    "storage",
    "network",
    "lp",
]

def add_user():
    os.system("clear")
    users = configuration_config._config.setdefault("user_account", {})

    print("\n-*- Add User -*-")

    # Set username
    while True:
        username = input("Username: ").strip()

        if not username:
            print("Username cannot be empty!")
        elif username in users:
            print("User already exists!")
        else:
            break

    # Set password
    while True:
        password = getpass("Password: ")
        confirm = getpass("Confirm Password: ")

        if not password:
            print("Password cannot be empty!")
        elif password != confirm:
            print("Passwords do not match!")
        else:
            break

    # Allow user choose group
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
                invalid_groups.append(g)
        if invalid_groups:
            print(f"Warning: invalid groups ignored → {' '.join(invalid_groups)}")

    # Save user in dictionary of user_accounts
    users[username] = {
        "password": password,
        "group": groups
    }

    print(f"\nUser '{username}' added successfully!")

def user_account_status():
    users = configuration_config._config.get("user_account", {})

    if not users:
        return "User accounts: Not set"

    lines = ["User accounts:"]

    for idx, (username, info) in enumerate(users.items(), start=1):
        password_status = "Already set" if info.get("password") else "Not set"

        raw_groups = info.get("group") or []
        valid = [g for g in raw_groups if g in _user_account_group]
        invalid = [g for g in raw_groups if g not in _user_account_group]

        group_display = ", ".join(valid) if valid else "Not set"

        if invalid:
            group_display += f" (invalid: {', '.join(invalid)})"

        lines.extend([
            "",
            f"{idx}. {username}",
            f"   Password: {password_status}",
            f"   Groups: {group_display}",
        ])

    return "\n".join(lines)

def configure_user():
    os.system("clear")
    users = configuration_config._config.get("user_account", {})

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

        # Change name for user
        if choice == "1":
            confirm = Confirm.ask("[yellow bold]Are you sure[/yellow bold] to [red bold]rename user?[/red bold]")
            if confirm:
                while True:
                    new_name = input("New username: ").strip()

                    if not new_name:
                        print("Cannot be empty!")
                    elif new_name in users:
                        print("User already exists!")
                    else:
                        break
                users[new_name] = users.pop(username)
                print(f"Renamed '{username}' → '{new_name}'")
                username = new_name  # update current context
            else:
                return

        # Change password for user
        elif choice == "2":
            confirm = Confirm.ask("[yellow bold]Are you sure[/yellow bold] to [red bold]change password user?[/red bold]")
            if confirm:
                while True:
                    password = getpass("New password: ")
                    confirm = getpass("Confirm password: ")

                    if not password:
                        print("Password cannot be empty!")
                    elif password != confirm:
                        print("Passwords do not match!")
                    else:
                        break
                users[username]["password"] = password
                print("Password updated!")
            else:
                return

        # Change group for user
        elif choice == "3":
            confirm = Confirm.ask("[yellow bold]Are you sure[/yellow bold] to [red bold]change group user?[/red bold]")
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
                        print(f"Warning: ignored → {' '.join(invalid)}")
                users[username]["group"] = groups
                print("Groups updated!")
            else:
                return

        # Remove user account
        elif choice == "4":
            confirm = input(f"Delete '{username}'? (y/n): ").lower()
            if confirm == "y":
                confirm_again = Confirm.ask("[yellow bold]Hey! you sure to remove this user account?[/yellow bold]")
                if confirm_again:
                    users.pop(username)
                    print("User deleted!")
                    break
            else:
                print("Cancelled.")

        # Return back to menu
        elif choice == "0":
            break

        else:
            print("Invalid option!")