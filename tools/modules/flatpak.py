from . import immutable_os_config
import os

def apply_flatpak_options():
    list_packages = ["flatpak"]

    option = immutable_os_config._config["features"]["flatpak"]
    match option:
        case "Enabled":
            try:
                for package in list_packages:
                    immutable_os_config._config["packages"]["list_packages"].append(package)
            except ValueError:
                pass

        case "Disabled":
            try:
                for package in list_packages:
                    immutable_os_config._config["packages"]["list_packages"].remove(package)
            except ValueError:
                pass
        case "Not set":
            try:
                for package in list_packages:
                    immutable_os_config._config["packages"]["list_packages"].remove(package)
            except ValueError:
                pass


def choose_flatpak_options():
    # List selection for toggle flatpak
    _flatpak_option_list = ["Disabled", "Enabled"]

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
                apply_flatpak_options()
                break

        # Select with text
        for opt in _flatpak_option_list:
            if choice == opt.lower():
                immutable_os_config._config["features"]["flatpak"] = opt
                apply_flatpak_options()
                return

        print("Invalid choice! Please try again.")