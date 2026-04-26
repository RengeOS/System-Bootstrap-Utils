import os
from . import immutable_os_config

def apply_chipset_options():
    list_intel_packages = ["mesa", "xf86-video-intel", "vulkan-intel", "intel-media-driver", "vulkan-headers", "vulkan-tools"]
    list_amd_packages = ["mesa", "xf86-video-amdgpu", "vulkan-radeon", "linux-firmware-amdgpu", "vulkan-headers", "vulkan-tools"]
    list_both_packages = list(set(list_intel_packages) | set(list_amd_packages)) # Combine them and avoid duplicate values ​​in the list

    config_packages = immutable_os_config._config["packages"]["list_packages"]

    option = immutable_os_config._config["system"]["chipset"]
    match option:
        case "Intel":
            try: 
                for package in list_intel_packages:
                    if package not in config_packages:
                        config_packages.append(package)

                for package in list_amd_packages:
                    if package in config_packages:
                        config_packages.remove(package)

            except ValueError:
                pass

def choose_chipset_options():
    # List selection for toggle flatpak
    _chipset_option_list = ["Intel", "AMD", "Both", "Manual"]

    os.system("clear")
    while True:
        print("\nAvailable options:")
        for i, opt in enumerate(_chipset_option_list, 1):
            print(f"{i}. {opt}")

        choice = input("\nEnter option (name or number): ").strip().lower()

        # Select with number
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(_chipset_option_list):
                immutable_os_config._config["system"]["chipset"] = _chipset_option_list[idx]
                break

        # Select with text
        for opt in _chipset_option_list:
            if choice == opt.lower():
                immutable_os_config._config["system"]["chipset"] = opt
                return

        print("Invalid choice! Please try again.")