from . import immutable_os_config
import os


def apply_profile_options():
    list_gnome_packages = ["gnome-extra", "gnome-browser-connector", "gnome-shell-extensions"]
    list_gnome_services = ["gdm"]

    # Config
    config_packages = immutable_os_config._config["packages"]["list_packages"]
    config_enabled_services = immutable_os_config._config["services"]["list_enabled_services"]

    option = immutable_os_config._config["system"]["profile"]
    match option:
        case "Gnome":
            try:
                for package in list_gnome_packages:
                    if package not in config_packages:
                        config_packages.append(package)
                
                for service in list_gnome_services:
                    if service not in config_enabled_services:
                        config_enabled_services.append(service)

            except ValueError:
                pass
        
        case "Manual" | "Not set":
            try:
                for package in list_gnome_packages:
                    if package in config_packages:
                        config_packages.remove(package)
                    
                for service in list_gnome_services:
                    if service in config_enabled_services:
                        config_enabled_services.remove(service)
            
            except ValueError:
                pass

def choose_profile_options():
    # List selection for profile
    _profile_option_list = ["Manual", "Gnome"]
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
                immutable_os_config._config["system"]["profile"] = _profile_option_list[idx]
                apply_profile_options()
                break

        # Select with text
        for opt in _profile_option_list:
            if choice == opt.lower():
                immutable_os_config._config["system"]["profile"] = opt
                apply_profile_options()
                return

        print("Invalid choice! Please try again.")