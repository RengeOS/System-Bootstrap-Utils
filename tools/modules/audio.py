from . import immutable_os_config
import os

def apply_audio_options():
    list_pipewire_packages = [
    "pipewire", "wireplumber", "pipewire-audio",
    "pipewire-alsa", "pipewire-pulse", "pipewire-jack",
    "pavucontrol", "pipewire-roc", "pipewire-v4l2"]

    list_pulse_audio_packages = [
    "pulseaudio", "pulseaudio-alsa", "pulseaudio-bluetooth",
    "pulseaudio-equalizer", "pulseaudio-jack", "pulseaudio-lirc",
    "pulseaudio-zeroconf"]

    config_packages = immutable_os_config._config["packages"]["list_packages"]

    option = immutable_os_config._config["system"]["audio"]
    match option:
        # Enabled pipewire
        case "Pipewire":
            try:
                for package in list_pipewire_packages:
                    if package not in config_packages:
                        config_packages.append(package)

                for package in list_pulse_audio_packages:
                    if package in config_packages:
                        config_packages.remove(package)

            except ValueError:
                pass
        # Enabled pulseaudio
        case "Pulse_Audio":
            try:
                for package in list_pulse_audio_packages:
                    if package not in config_packages:
                        config_packages.append(package)

                for package in list_pipewire_packages:
                    if package in config_packages:
                        config_packages.remove(package)

            except ValueError:
                pass
        # Disabled all
        case "Manual" | "Not set":
            try:
                for package in list_pipewire_packages:
                    if package in config_packages:
                        config_packages.remove(package)

                for package in list_pulse_audio_packages:
                    if package in config_packages:
                        config_packages.remove(package)
                        
            except ValueError:
                pass

def choose_audio_options():
    # List selection for toggle audio
    _audio_option_list = ["Pipewire", "Pulse_Audio", "Manual"]
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
                apply_audio_options()
                break

        # Select with text
        for opt in _audio_option_list:
            if choice == opt.lower():
                immutable_os_config._config["system"]["audio"] = opt
                apply_audio_options()
                return

        print("Invalid choice! Please try again.")