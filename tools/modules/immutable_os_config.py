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

    "deployment": {
        "next_slot": "Not set",
        # How it will look like after configuration:
        # "next-slot": "slot_a", # or slot_b
    },

    "commands_in_chroot": {
        "list_commands": [],
        "list_executable_scripts": [],
    },

    "packages": {
        "list_packages": [],
        "list_aur_packages": [],
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