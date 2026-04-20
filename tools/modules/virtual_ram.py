from . import immutable_os_config
import os

# List supported virtual ram
_virtual_ram_list = ["Disabled", "Swap", "Swap-to-file", "Zram"]


def choose_virtual_ram_options():
    os.system("clear")
    while True:
        print("\nAvailable Virtual RAM options:")
        for i, opt in enumerate(_virtual_ram_list, 1):
            print(f"{i}. {opt}")

        choice = input("\nEnter option (name or number): ").strip().lower()

        # Select with number
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(_virtual_ram_list):
                immutable_os_config._config["features"]["virtual_ram"] = _virtual_ram_list[idx]
                break

        # Select with text
        for opt in _virtual_ram_list:
            if choice == opt.lower():
                immutable_os_config._config["features"]["virtual_ram"] = opt
                return

        print("Invalid choice! Please try again.")