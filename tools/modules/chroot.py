import os
from . import immutable_os_config

def edit_commands_in_chroot():
    while True:
        
        os.system("clear")
        list_commands = immutable_os_config._config["commands_in_chroot"]["list_commands"]
        list_executable_scripts = immutable_os_config._config["commands_in_chroot"]["list_executable_scripts"]

        print(f"Commands           : {list_commands}")
        print(f"Executable Scripts : {list_executable_scripts}")
        print("\n0. Back")
        print("1. Add command")
        print("2. Edit command")
        print("3. Delete command")
        print("4. Add executable script")
        print("5. Edit executable script")
        print("6. Delete executable script")

        choice = input("\nEnter option: ").strip()

        if choice == "0":
            return

        elif choice == "1":
            cmd = input("Enter command(s) (comma-separated): ").strip()
            if not cmd:
                print("No input provided.")
                input("Press Enter to continue...")
                continue
            for c in cmd.split(","):
                c = c.strip()
                if not c:
                    continue
                if c in list_commands:
                    print(f"'{c}' already exists, skipped.")
                else:
                    list_commands.append(c)
                    print(f"Added '{c}'.")
            input("Press Enter to continue...")

        elif choice == "2":
            cmd_name = input("Enter command to edit: ").strip()
            if not cmd_name:
                print("No input provided.")
                input("Press Enter to continue...")
                continue
            if cmd_name not in list_commands:
                print(f"'{cmd_name}' not found.")
                input("Press Enter to continue...")
                continue
            new_cmd = input(f"Enter new command for '{cmd_name}': ").strip()
            if not new_cmd:
                print("Empty input, cancelled.")
                input("Press Enter to continue...")
                continue
            list_commands[list_commands.index(cmd_name)] = new_cmd
            print(f"Updated '{cmd_name}' → '{new_cmd}'.")
            input("Press Enter to continue...")

        elif choice == "3":
            raw = input("Enter command(s) to delete (comma-separated): ").strip()
            if not raw:
                print("No input provided.")
                input("Press Enter to continue...")
                continue
            for c in raw.split(","):
                c = c.strip()
                if not c:
                    continue
                if c in list_commands:
                    list_commands.remove(c)
                    print(f"Deleted '{c}'.")
                else:
                    print(f"'{c}' not found.")
            input("Press Enter to continue...")

        elif choice == "4":
            raw = input("Enter executable script(s) (comma-separated): ").strip()
            if not raw:
                print("No input provided.")
                input("Press Enter to continue...")
                continue
            for s in raw.split(","):
                s = s.strip()
                if not s:
                    continue
                if s in list_executable_scripts:
                    print(f"'{s}' already exists, skipped.")
                else:
                    list_executable_scripts.append(s)
                    print(f"Added '{s}'.")
            input("Press Enter to continue...")

        elif choice == "5":
            script_name = input("Enter executable script to edit: ").strip()
            if not script_name:
                print("No input provided.")
                input("Press Enter to continue...")
                continue
            if script_name not in list_executable_scripts:
                print(f"'{script_name}' not found.")
                input("Press Enter to continue...")
                continue
            new_script = input(f"Enter new script for '{script_name}': ").strip()
            if not new_script:
                print("Empty input, cancelled.")
                input("Press Enter to continue...")
                continue
            list_executable_scripts[list_executable_scripts.index(script_name)] = new_script
            print(f"Updated '{script_name}' → '{new_script}'.")
            input("Press Enter to continue...")

        elif choice == "6":
            raw = input("Enter executable script(s) to delete (comma-separated): ").strip()
            if not raw:
                print("No input provided.")
                input("Press Enter to continue...")
                continue
            for s in raw.split(","):
                s = s.strip()
                if not s:
                    continue
                if s in list_executable_scripts:
                    list_executable_scripts.remove(s)
                    print(f"Deleted '{s}'.")
                else:
                    print(f"'{s}' not found.")
            input("Press Enter to continue...")

        else:
            print("Invalid choice! Please enter 0-6.")
            input("Press Enter to continue...")