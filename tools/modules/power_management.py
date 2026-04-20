from . import immutable_os_config
import os

# List selection for power management
_power_management_option_list = ["Disabled", "Tuned", "Power-profiles-daemon"]


def choose_power_management_options():
    os.system("clear")
    while True:
        print("\nAvailable options:")
        for i, opt in enumerate(_power_management_option_list, 1):
            print(f"{i}. {opt}")

        choice = input("\nEnter option (name or number): ").strip().lower()

        # Select with number
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(_power_management_option_list):
                immutable_os_config._config["features"]["power_management"] = _power_management_option_list[idx]
                break

        # Select with text
        for opt in _power_management_option_list:
            if choice == opt.lower():
                immutable_os_config._config["features"]["power_management"] = opt
                return

        print("Invalid choice! Please try again.")