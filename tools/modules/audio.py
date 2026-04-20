from . import immutable_os_config
import os

# List selection for toggle audio
_audio_option_list = ["Pipewire", "Pulse-audio"]


def choose_audio_options():
    os.system("clear")
    while True:
        print("\nAvailable options:")
        for i, opt in enumerate(_audio_option_list, 1):
            print(f"{i}. {opt}")

        choice = input("\nEnter option (name or number): ").strip().lower()

        # Select with number
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(_audio_option_list):
                immutable_os_config._config["system"]["audio"] = _audio_option_list[idx]
                break

        # Select with text
        for opt in _audio_option_list:
            if choice == opt.lower():
                immutable_os_config._config["system"]["audio"] = opt
                return

        print("Invalid choice! Please try again.")