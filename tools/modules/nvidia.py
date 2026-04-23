from . import immutable_os_config
import os

def apply_nvidia_options():
    list_packages = ["nvidia-open-dkms", "nvidia-utils", "libglvnd", "xf86-video-nouveau"]

    option = immutable_os_config._config["features"]["nvidia"]
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
    
def choose_nvidia_options():
    # List selection for toggle nvidia supported
    _nvidia_option_list = ["Disabled", "Enabled"]

    os.system("clear")
    while True:
        print("\nAvailable options:")
        for i, opt in enumerate(_nvidia_option_list, 1):
            print(f"{i}. {opt}")

        choice = input("\nEnter option (name or number): ").strip().lower()

        # Select with number
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(_nvidia_option_list):
                immutable_os_config._config["features"]["nvidia"] = _nvidia_option_list[idx]
                apply_nvidia_options()
                break

        # Select with text
        for opt in _nvidia_option_list:
            if choice == opt.lower():
                immutable_os_config._config["features"]["nvidia"] = opt
                apply_nvidia_options()
                return

        print("Invalid choice! Please try again.")


def setup_nvidia():
    path                = "/etc/mkinitcpio.conf"
    nvidia_modules_list = ["nvidia", "nvidia_modeset", "nvidia_uvm", "nvidia_drm"]
    lines               = open(path).readlines()

    for i in range(len(lines)):
        if lines[i].startswith("MODULES="):
            start   = lines[i].find("(")
            end     = lines[i].find(")")
            modules = lines[i][start+1 : end].split()
            for module in nvidia_modules_list:
                if module not in modules:
                    modules.append(module)
            content  = " ".join(modules)
            lines[i] = f"MODULES=({content})\n"
            
    open(path, "w").writelines(lines)