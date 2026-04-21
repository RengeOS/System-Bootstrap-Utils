import os
from . import immutable_os_config

def edit_packages():
    os.system("clear")

    def parse_packages(raw):
        return [p for p in raw.strip().split() if p]

    while True:
        os.system("clear")
        list_packages = immutable_os_config._config["packages"]["list_packages"]
        list_aur_packages = immutable_os_config._config["packages"]["list_aur_packages"]
        print(f"Current packages: {list_packages}")
        print(f"Current AUR packages: {list_aur_packages}\n")

        print("\n0. Back")
        print("1. Add packages")
        print("2. Add AUR packages")
        print("3. Edit package")
        print("4. Delete package")

        choice = input("\nEnter option: ").strip()

        # Back
        if choice == "0":
            return

        # Add packages
        if choice == "1":
            packages = parse_packages(input("Enter package(s): "))
            if packages:
                list_packages.extend(packages)

        # Add AUR packages
        elif choice == "2":
            packages = parse_packages(input("Enter AUR package(s): "))
            if packages:
                list_aur_packages.extend(packages)

        # Edit package
        elif choice == "3":
            while True:
                print("\n0. Back")
                for i, pkg in enumerate(list_packages, 1):
                    print(f"{i}. [Package] {pkg}")
                for i, pkg in enumerate(list_aur_packages, len(list_packages) + 1):
                    print(f"{i}. [AUR] {pkg}")

                idx = input("Enter number to edit: ").strip()
                if idx == "0":
                    break
                if idx.isdigit():
                    idx = int(idx) - 1
                    if idx < len(list_packages):
                        new_pkg = input("Enter new package name: ").strip()
                        if new_pkg:
                            list_packages[idx] = new_pkg
                        break
                    elif idx < len(list_packages) + len(list_aur_packages):
                        new_pkg = input("Enter new package name: ").strip()
                        if new_pkg:
                            list_aur_packages[idx - len(list_packages)] = new_pkg
                        break
                print("Invalid choice! Please try again.")

        # Delete package
        elif choice == "4":
            while True:
                print("\n0. Back")
                for i, pkg in enumerate(list_packages, 1):
                    print(f"{i}. [Package] {pkg}")
                for i, pkg in enumerate(list_aur_packages, len(list_packages) + 1):
                    print(f"{i}. [AUR] {pkg}")

                idx = input("Enter number to delete: ").strip()
                if idx == "0":
                    break
                if idx.isdigit():
                    idx = int(idx) - 1
                    if idx < len(list_packages):
                        list_packages.pop(idx)
                        break
                    elif idx < len(list_packages) + len(list_aur_packages):
                        list_aur_packages.pop(idx - len(list_packages))
                        break
                print("Invalid choice! Please try again.")

        else:
            print("Invalid choice! Please try again.")