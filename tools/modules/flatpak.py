from . import immutable_os_config
import os

# List selection for toggle flatpak
_flatpak_option_list = ["Disabled", "Enabled"]


def choose_flatpak_options():
    os.system("clear")
    while True:
        print("\nAvailable options:")
        for i, opt in enumerate(_flatpak_option_list, 1):
            print(f"{i}. {opt}")

        choice = input("\nEnter option (name or number): ").strip().lower()

        # Select with number
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(_flatpak_option_list):
                immutable_os_config._config["features"]["flatpak"] = _flatpak_option_list[idx]
                break

        # Select with text
        for opt in _flatpak_option_list:
            if choice == opt.lower():
                immutable_os_config._config["features"]["flatpak"] = opt
                return

        print("Invalid choice! Please try again.")