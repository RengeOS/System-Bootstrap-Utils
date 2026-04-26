from . import immutable_os_config
import os

def apply_power_management_options():

    # Config
    config_enabled_services = immutable_os_config._config["services"]["list_enabled_services"]
    config_packages = immutable_os_config._config["packages"]["list_packages"]

    # Tuned
    list_tuned_packages = ["tuned", "tuned-ppd"]
    list_tuned_services = ["tuned", "tuned-ppd"]

    # Power Profiles Daemon
    list_power_profiles_daemon_packages = ["power-profiles-daemon"]
    list_power_profiles_daemon_services = ["power-profiles-daemon"]

    option = immutable_os_config._config["features"]["power_management"]
    match option:
        case "Tuned":
            try:
                # Enabled Tuned
                for package in list_tuned_packages:
                    if package not in config_packages:
                        config_packages.append(package)

                for service in list_tuned_services:
                        if service not in config_enabled_services:
                            config_enabled_services.append(service)

                # Disabled Power_Profiles_Daemon
                for package in list_power_profiles_daemon_packages:
                    if package in config_packages:
                        config_packages.remove(package)

                for service in list_power_profiles_daemon_services:
                    if service in config_enabled_services:
                        config_enabled_services.remove(service)

            except ValueError:
                pass

        case "Power_Profiles_Daemon":
            try:
                # Enabled Power_Profiles_Daemon
                for package in list_power_profiles_daemon_packages:
                    if package not in config_packages:
                        config_packages.append(package)
                
                for service in list_power_profiles_daemon_services:
                    if service not in config_enabled_services:
                        config_enabled_services.append(service)
                
                # Disabled Tuned
                for package in list_tuned_packages:
                    if package in config_packages:
                        config_packages.remove(package)

                for service in list_tuned_services:
                    if service in config_enabled_services:
                        config_enabled_services.remove(service)
                
            except ValueError:
                pass

        case "Disabled" | "Not set":
            try:
                # Disabled Tuned
                for package in list_tuned_packages:
                    if package in config_packages:
                        config_packages.remove(package)
                
                for service in list_tuned_services:
                    if service in config_enabled_services:
                        config_enabled_services.remove(service)
                
                # Disabled Power_Profiles_Daemon
                for package in list_power_profiles_daemon_packages:
                    if package in config_packages:
                        config_packages.remove(package)
                
                for service in list_power_profiles_daemon_services:
                    if service in config_enabled_services:
                        config_enabled_services.remove(service)

            except ValueError:
                pass

def choose_power_management_options():

    # List selection for power management
    _power_management_option_list = ["Disabled", "Tuned", "Power_Profiles_Daemon"]

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
                apply_power_management_options()
                break

        # Select with text
        for opt in _power_management_option_list:
            if choice == opt.lower():
                immutable_os_config._config["features"]["power_management"] = opt
                apply_power_management_options()
                return

        print("Invalid choice! Please try again.")