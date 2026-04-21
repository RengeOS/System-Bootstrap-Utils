from . import immutable_os_config
import os

# List selection for toggle waydroid
_next_slot_option_list = ["Slot_A", "Slot_B"]


def choose_next_slot_options():
    os.system("clear")
    while True:
        print("\nAvailable options:")
        for i, opt in enumerate(_next_slot_option_list, 1):
            print(f"{i}. {opt}")

        choice = input("\nEnter option (name or number): ").strip().lower()

        # Select with number
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(_next_slot_option_list):
                immutable_os_config._config["deployment"]["next_slot"] = _next_slot_option_list[idx]
                break

        # Select with text
        for opt in _next_slot_option_list:
            if choice == opt.lower():
                immutable_os_config._config["deployment"]["next_slot"] = opt
                return

        print("Invalid choice! Please try again.")