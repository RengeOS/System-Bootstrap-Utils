from . import immutable_os_config
import os

# List selection for toggle waydroid
_waydroid_option_list = ["Disabled", "Enabled"]

def apply_waydroid_options():
    list_waydroid_packages = ["waydroid"]
    list_waydroid_aur_packages = ["waydroid-image-gapps", "binder_linux-dkms"]
    list_waydroid_services = ["waydroid-container.service"]

    # Config
    config_packages = immutable_os_config._config["packages"]["list_packages"]
    config_aur_packages = immutable_os_config._config["package"]["list_aur_packages"]
    config_enabled_services = immutable_os_config._config["services"]["list_enabled_services"]

    option = immutable_os_config._config["features"]["waydroid"]

    match option:
            case "Enabled":
                try:
                    # Enabled waydroid
                    for package in list_waydroid_packages:
                        if package not in config_packages:
                            config_packages.append(package)

                    for package in list_waydroid_aur_packages:
                        if package not in config_aur_packages:
                            config_aur_packages.append(package)
                    
                    for service in list_waydroid_services:
                        if service not in config_enabled_services:
                            config_enabled_services.append(service)

                except ValueError:
                    pass

            case "Disabled" | "Not set":
                try:
                    for package in list_waydroid_packages:
                        if package in config_packages:
                            config_packages.remove(package)

                    for package in list_waydroid_aur_packages:
                        if package in config_aur_packages:
                            config_aur_packages.remove(package)
                    
                    for service in list_waydroid_services:
                        if service in config_enabled_services:
                            config_enabled_services.remove(package)

                except ValueError:
                    pass

def choose_waydroid_options():
    os.system("clear")
    while True:
        print("\nAvailable options:")
        for i, opt in enumerate(_waydroid_option_list, 1):
            print(f"{i}. {opt}")

        choice = input("\nEnter option (name or number): ").strip().lower()

        # Select with number
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(_waydroid_option_list):
                immutable_os_config._config["features"]["waydroid"] = _waydroid_option_list[idx]
                apply_waydroid_options()
                break

        # Select with text
        for opt in _waydroid_option_list:
            if choice == opt.lower():
                immutable_os_config._config["features"]["waydroid"] = opt
                apply_waydroid_options()
                return

        print("Invalid choice! Please try again.")