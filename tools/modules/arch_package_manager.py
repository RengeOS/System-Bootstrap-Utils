import os
from . import immutable_os_config

def edit_packages():
    while True:
        os.system("clear")
        list_packages = immutable_os_config._config["packages"]["list_packages"]
        list_aur_packages = immutable_os_config._config["packages"]["list_aur_packages"]

        print(f"Packages     : {list_packages}")
        print(f"AUR Packages : {list_aur_packages}")
        print("\n0. Back")
        print("1. Add packages")
        print("2. Add AUR packages")
        print("3. Edit package")
        print("4. Delete package")

        choice = input("\nEnter option: ").strip()

        if choice == "0":
            return

        elif choice == "1":
            raw = input("Enter package(s) (space-separated): ").strip()
            if not raw:
                print("No input provided.")
                input("Press Enter to continue...")
                continue
            for pkg in raw.split():
                if pkg in list_packages or pkg in list_aur_packages:
                    print(f"'{pkg}' already exists, skipped.")
                else:
                    list_packages.append(pkg)
                    print(f"Added '{pkg}'.")
            input("Press Enter to continue...")

        elif choice == "2":
            raw = input("Enter AUR package(s) (space-separated): ").strip()
            if not raw:
                print("No input provided.")
                input("Press Enter to continue...")
                continue
            for pkg in raw.split():
                if pkg in list_packages or pkg in list_aur_packages:
                    print(f"'{pkg}' already exists, skipped.")
                else:
                    list_aur_packages.append(pkg)
                    print(f"Added '{pkg}'.")
            input("Press Enter to continue...")

        elif choice == "3":
            pkg_name = input("Enter package name to edit: ").strip()
            if not pkg_name:
                print("No input provided.")
                input("Press Enter to continue...")
                continue
            if pkg_name in list_packages:
                new_name = input(f"Enter new name for '{pkg_name}': ").strip()
                if not new_name:
                    print("Empty input, cancelled.")
                elif new_name in list_packages or new_name in list_aur_packages:
                    print(f"'{new_name}' already exists.")
                else:
                    list_packages[list_packages.index(pkg_name)] = new_name
                    print(f"Updated '{pkg_name}' → '{new_name}'.")
            elif pkg_name in list_aur_packages:
                new_name = input(f"Enter new name for '{pkg_name}': ").strip()
                if not new_name:
                    print("Empty input, cancelled.")
                elif new_name in list_packages or new_name in list_aur_packages:
                    print(f"'{new_name}' already exists.")
                else:
                    list_aur_packages[list_aur_packages.index(pkg_name)] = new_name
                    print(f"Updated '{pkg_name}' → '{new_name}'.")
            else:
                print(f"'{pkg_name}' not found.")
            input("Press Enter to continue...")

        elif choice == "4":
            raw = input("Enter package name(s) to delete (space-separated): ").strip()
            if not raw:
                print("No input provided.")
                input("Press Enter to continue...")
                continue
            for pkg in raw.split():
                if pkg in list_packages:
                    list_packages.remove(pkg)
                    print(f"Deleted '{pkg}'.")
                elif pkg in list_aur_packages:
                    list_aur_packages.remove(pkg)
                    print(f"Deleted '{pkg}'.")
                else:
                    print(f"'{pkg}' not found.")
            input("Press Enter to continue...")

        else:
            print("Invalid choice! Please enter 0-4.")
            input("Press Enter to continue...")