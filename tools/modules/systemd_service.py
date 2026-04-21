import os
from . import immutable_os_config

def edit_systemd_services():
    os.system("clear")

    def parse_services(raw):
        services = raw.strip().split()
        return [s for s in services if s and all(c.isalnum() or c in "-_." for c in s)]

    def is_duplicate(service):
        if service in list_enabled:
            return "enabled"
        if service in list_disabled:
            return "disabled"
        return None

    while True:
        list_enabled = immutable_os_config._config["services"]["list_enabled_services"]
        list_disabled = immutable_os_config._config["services"]["list_disabled_services"]

        print("\n0. Back")
        print("1. Add enabled service")
        print("2. Add disabled service")
        print("3. Edit service")
        print("4. Delete service")

        choice = input("\nEnter option: ").strip()

        # Back
        if choice == "0":
            return

        # Add enabled service
        if choice == "1":
            services = parse_services(input("Enter service name(s): "))
            if not services:
                print("Invalid service name(s)! Please try again.")
                continue
            for service in services:
                duplicate = is_duplicate(service)
                if duplicate:
                    print(f"'{service}' is already in {duplicate} list! Skipping.")
                else:
                    list_enabled.append(service)

        # Add disabled service
        elif choice == "2":
            services = parse_services(input("Enter service name(s): "))
            if not services:
                print("Invalid service name(s)! Please try again.")
                continue
            for service in services:
                duplicate = is_duplicate(service)
                if duplicate:
                    print(f"'{service}' is already in {duplicate} list! Skipping.")
                else:
                    list_disabled.append(service)

        # Edit service
        elif choice == "3":
            while True:
                print("\n0. Back")
                for i, service in enumerate(list_enabled, 1):
                    print(f"{i}. [Enabled] {service}")
                for i, service in enumerate(list_disabled, len(list_enabled) + 1):
                    print(f"{i}. [Disabled] {service}")

                idx = input("Enter number to edit: ").strip()
                if idx == "0":
                    break
                if idx.isdigit():
                    idx = int(idx) - 1
                    if idx < len(list_enabled):
                        new_services = parse_services(input("Enter new service name: "))
                        if not new_services:
                            print("Invalid service name! Please try again.")
                            continue
                        duplicate = is_duplicate(new_services[0])
                        if duplicate:
                            print(f"'{new_services[0]}' is already in {duplicate} list! Please try again.")
                            continue
                        list_enabled[idx] = new_services[0]
                        break
                    elif idx < len(list_enabled) + len(list_disabled):
                        new_services = parse_services(input("Enter new service name: "))
                        if not new_services:
                            print("Invalid service name! Please try again.")
                            continue
                        duplicate = is_duplicate(new_services[0])
                        if duplicate:
                            print(f"'{new_services[0]}' is already in {duplicate} list! Please try again.")
                            continue
                        list_disabled[idx - len(list_enabled)] = new_services[0]
                        break
                print("Invalid choice! Please try again.")

        # Delete service
        elif choice == "4":
            while True:
                print("\n0. Back")
                for i, service in enumerate(list_enabled, 1):
                    print(f"{i}. [Enabled] {service}")
                for i, service in enumerate(list_disabled, len(list_enabled) + 1):
                    print(f"{i}. [Disabled] {service}")

                idx = input("Enter number to delete: ").strip()
                if idx == "0":
                    break
                if idx.isdigit():
                    idx = int(idx) - 1
                    if idx < len(list_enabled):
                        list_enabled.pop(idx)
                        break
                    elif idx < len(list_enabled) + len(list_disabled):
                        list_disabled.pop(idx - len(list_enabled))
                        break
                print("Invalid choice! Please try again.")

        else:
            print("Invalid choice! Please try again.")