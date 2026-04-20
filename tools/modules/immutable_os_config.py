# The configuration value will be stored here as a dictionary of python:)
# It's best not to touch this unless you understand what it's doing!
_config = {
    "system": {
        "hostname": "Not set",
        "timezone": "Not set",
        "system_locale": "Not set",
        "profile": "Not set",
        "audio": "Not set"
    },
    "accounts": {
        "root": {
            "password": "Not set",
        },
        "users": {
            # How it will look like after configuration:
            # "name_user": {
            #     "password": "abcxyz",
            #     "group": ["wheel", "audio"],
            # }
        },
    },
    "disk": {
        "layout": {
            "efi_partition": "Not set",
            "data_partition": "Not set",
            "repair_partition": "Not set",
            "boot_a_partition": "Not set",
            "boot_b_partition": "Not set",
            "root_a_partition": "Not set",
            "root_b_partition": "Not set",
            "swap_partition": "Not set",
        },

        "mount": {
            # How it will look like after configuration:
            # "/dev/sda5": {
            # "mount_point": "/home",
            # "fstype": "ext4",
            # "options": "defaults",
            # "dump": 0,
            # "pass": 0,
            # },
        },
    },

    "slot_status": {
        "slot-a": "Not set",
        "slot-b": "Not set",
    },

    "commands_in_chroot": {
        "list_commands": [],
    },

    "packages": {
        "list_packages": [],
        "list_aur_packages": [],
        # Example: 
        # list_git_packages: [https://github.com/RengeOS/PKGBUILD, "./path to folder contain PKGBUILD file"]
        "list_git_packages": [],
    },

    "services": {
        "list_enabled_services": [],
        "list_disabled_services": [],
    },
    
    "features": {
        "virtual_ram": "Not set",
        "nvidia": "Not set",
        "waydroid": "Not set",
        "flatpak": "Not set",
        "bluetooth": "Not set",
        "power_management": "Not set",
    },
}