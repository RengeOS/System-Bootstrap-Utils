import os
from . import immutable_os_config

def edit_commands_in_chroot():
    os.system("clear")
    while True:
        os.system("clear")
        list_commands = immutable_os_config._config["commands_in_chroot"]["list_commands"]

        print("\n0. Back")
        print("1. Add command")
        print("2. Edit command")
        print("3. Delete command")

        choice = input("\nEnter option: ").strip()

        # Back
        if choice == "0":
            return

        # Add command
        if choice == "1":
            cmd = input("Enter command(s): ").strip()
            if cmd:
                list_commands.extend([c.strip() for c in cmd.split(",")])

        # Edit command
        elif choice == "2":
            while True:
                print("\n0. Back")
                for i, cmd in enumerate(list_commands, 1):
                    print(f"{i}. {cmd}")
                idx = input("Enter number to edit: ").strip()
                if idx == "0":
                    break
                if idx.isdigit() and 0 <= int(idx) - 1 < len(list_commands):
                    new_cmd = input("Enter new command: ").strip()
                    if new_cmd:
                        list_commands[int(idx) - 1] = new_cmd
                    break
                print("Invalid choice! Please try again.")

        # Delete command
        elif choice == "3":
            while True:
                print("\n0. Back")
                for i, cmd in enumerate(list_commands, 1):
                    print(f"{i}. {cmd}")
                idx = input("Enter number to delete: ").strip()
                if idx == "0":
                    break
                if idx.isdigit() and 0 <= int(idx) - 1 < len(list_commands):
                    list_commands.pop(int(idx) - 1)
                    break
                print("Invalid choice! Please try again.")

        else:
            print("Invalid choice! Please try again.")