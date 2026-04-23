import os
from . import immutable_os_config

def choose_chipset_options():
    # List selection for toggle flatpak
    _chipset_option_list = ["Intel", "AMD", "Both", "Manual"]

    os.system("clear")
    while True:
        print("\nAvailable options:")
        for i, opt in enumerate(_chipset_option_list, 1):
            print(f"{i}. {opt}")

        choice = input("\nEnter option (name or number): ").strip().lower()

        # Select with number
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(_chipset_option_list):
                immutable_os_config._config["system"]["chipset"] = _chipset_option_list[idx]
                break

        # Select with text
        for opt in _chipset_option_list:
            if choice == opt.lower():
                immutable_os_config._config["system"]["chipset"] = opt
                return

        print("Invalid choice! Please try again.")