import os
from . import immutable_os_config

def edit_systemd_services():
    while True:
        os.system("clear")
        list_enabled = immutable_os_config._config["services"]["list_enabled_services"]
        list_disabled = immutable_os_config._config["services"]["list_disabled_services"]

        print(f"Enabled  : {list_enabled}")
        print(f"Disabled : {list_disabled}")
        print("\n0. Back")
        print("1. Add enabled service")
        print("2. Add disabled service")
        print("3. Edit service")
        print("4. Delete service")

        choice = input("\nEnter option: ").strip()

        if choice == "0":
            return

        elif choice == "1":
            raw = input("Enter service name(s) (space-separated): ").strip()
            if not raw:
                print("No input provided.")
                input("Press Enter to continue...")
                continue
            for svc in raw.split():
                if not all(c.isalnum() or c in "-_." for c in svc):
                    print(f"'{svc}' is invalid, only alphanumeric, '-', '_', '.' allowed. Skipped.")
                elif svc in list_enabled or svc in list_disabled:
                    print(f"'{svc}' already exists, skipped.")
                else:
                    list_enabled.append(svc)
                    print(f"Added '{svc}' to enabled list.")
            input("Press Enter to continue...")

        elif choice == "2":
            raw = input("Enter service name(s) (space-separated): ").strip()
            if not raw:
                print("No input provided.")
                input("Press Enter to continue...")
                continue
            for svc in raw.split():
                if not all(c.isalnum() or c in "-_." for c in svc):
                    print(f"'{svc}' is invalid, only alphanumeric, '-', '_', '.' allowed. Skipped.")
                elif svc in list_enabled or svc in list_disabled:
                    print(f"'{svc}' already exists, skipped.")
                else:
                    list_disabled.append(svc)
                    print(f"Added '{svc}' to disabled list.")
            input("Press Enter to continue...")

        elif choice == "3":
            svc_name = input("Enter service name to edit: ").strip()
            if not svc_name:
                print("No input provided.")
                input("Press Enter to continue...")
                continue
            if svc_name in list_enabled:
                new_name = input(f"Enter new name for '{svc_name}': ").strip()
                if not new_name:
                    print("Empty input, cancelled.")
                elif not all(c.isalnum() or c in "-_." for c in new_name):
                    print(f"'{new_name}' is invalid, only alphanumeric, '-', '_', '.' allowed.")
                elif new_name in list_enabled or new_name in list_disabled:
                    print(f"'{new_name}' already exists.")
                else:
                    list_enabled[list_enabled.index(svc_name)] = new_name
                    print(f"Updated '{svc_name}' → '{new_name}'.")
            elif svc_name in list_disabled:
                new_name = input(f"Enter new name for '{svc_name}': ").strip()
                if not new_name:
                    print("Empty input, cancelled.")
                elif not all(c.isalnum() or c in "-_." for c in new_name):
                    print(f"'{new_name}' is invalid, only alphanumeric, '-', '_', '.' allowed.")
                elif new_name in list_enabled or new_name in list_disabled:
                    print(f"'{new_name}' already exists.")
                else:
                    list_disabled[list_disabled.index(svc_name)] = new_name
                    print(f"Updated '{svc_name}' → '{new_name}'.")
            else:
                print(f"'{svc_name}' not found.")
            input("Press Enter to continue...")
            
        elif choice == "4":
            raw = input("Enter service name(s) to delete (space-separated): ").strip()
            if not raw:
                print("No input provided.")
                input("Press Enter to continue...")
                continue
            for svc in raw.split():
                if svc in list_enabled:
                    list_enabled.remove(svc)
                    print(f"Deleted '{svc}'.")
                elif svc in list_disabled:
                    list_disabled.remove(svc)
                    print(f"Deleted '{svc}'.")
                else:
                    print(f"'{svc}' not found.")
            input("Press Enter to continue...")
        else:
            print("Invalid choice! Please enter 0-4.")
            input("Press Enter to continue...")