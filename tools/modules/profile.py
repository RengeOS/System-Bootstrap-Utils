from . import configuration_config
import os

# List selection for profile
_profile_option_list = ["Minimal", "Gnome"]


def choose_profile_options():
    os.system("clear")
    while True:
        print("\nAvailable options:")
        for i, opt in enumerate(_profile_option_list, 1):
            print(f"{i}. {opt}")

        choice = input("\nEnter option (name or number): ").strip().lower()

        # Select with number
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(_profile_option_list):
                configuration_config._config["profile"] = _profile_option_list[idx]
                break

        # Select with text
        for opt in _profile_option_list:
            if choice == opt.lower():
                configuration_config._config["profile"] = opt
                return

        print("Invalid choice! Please try again.")