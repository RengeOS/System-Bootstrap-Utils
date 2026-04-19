import os
import re
from getpass import getpass
import subprocess
from .modules import get_information, drawer, system_locale, hostname, timezone, root_password, user_account, virtual_ram, configuration_config, nvidia, waydroid, flatpak, disk
from rich import print
from rich.prompt import Prompt, Confirm
import subprocess, json

def exit_installer():
    os.system("clear")
    confirm = Confirm.ask("Are you sure you want to exit the installer?")
    if confirm:
        os.system("clear")
        raise SystemExit(0)


def run_installer():
    os.system("clear")
    confirm = Confirm.ask("Are you sure you want to run the installer?")
    if confirm:
        os.system("clear")
        raise SystemExit(0)

def main():
    # Check whether you have UEFI or LEGACY BIOS before running as LEGACY BIOS is not supported:(
    boot_mode, boot_filesystem_supported = get_information.get_boot_mode_information()
    if boot_mode == "LEGACY":
        print(f"\n[green bold]Your current boot mode:[/green bold] [purple bold]{boot_mode}[/purple bold]")
        print(f"\n[yellow bold]The Immutable OS method only supports UEFI devices:(\n\n>_Notes: You can use the Mutable OS method instead:D[/yellow bold]")
        raise SystemExit(0)

    menu = [
        {
            "label":     "Hostname",
            "info":      lambda: f"Current hostname: {configuration_config._config['hostname']}\n\nPress ENTER to change.",
            "on_select": hostname.set_hostname,
            "children":  [],
        },
        {
            "label":     "Timezone and System Locale",
            "info":      lambda: f"""Current timezone: {configuration_config._config['timezone']}
                                     Current system locale: {configuration_config._config['system_locale']}
                                  
                                  Press Enter to change the Timezone and System locale.""",
            "on_select": None,
            "children": [
                        {
                            "label":     "Timezone",
                            "info":      lambda: f"Current timezone: {configuration_config._config['timezone']}\n\nPress ENTER to change.",
                            "on_select": timezone.set_timezone,
                            "children":  [],
                        },
                        {
                            "label":     "System Locale",
                            "info":      lambda: f"Current system locale: {configuration_config._config['system_locale']}\n\nPress ENTER to change.",
                            "on_select": system_locale.set_locale,
                            "children":  [],
                        },
            ],
        },
        {
            "label":     "Disks",
            "info":      lambda: f"""Current disk method: {configuration_config._config['disk']['method']}

                                  Disk info:
                                  {disk.show_disk_info()
                                  
                                  }""",
            "on_select": None,
            "children":  [
                        {
                            "label":     "Choose disk method",
                            "info":      lambda: f"Current disk method: {configuration_config._config['disk']['method']}\n\nPress ENTER to change.",
                            "on_select": disk.choose_disk_method,
                            "children":  [],
                        },
            ],
        },
        {
            "label":     "User account",
            "info":      lambda: f"{user_account.user_account_status()}",
            "on_select": None,
            "children":  [
                        {
                            "label":     "Add user account",
                            "info":      lambda: f"{user_account.user_account_status()}\n\nPress Enter to add user account",
                            "on_select": user_account.add_user,
                            "children":  [],
                        },
                        {
                            "label":     "Configuration user account",
                            "info":      lambda: f"{user_account.user_account_status()}\n\nPress Enter to configuration user account",
                            "on_select": user_account.configure_user,
                            "children":  [],
                        },
            ],    
        },
        {
            "label":     "Root password",
            "info":      lambda: f"Root password status: " f"{'Already set' if configuration_config._config['root_password'] != 'Not set' else 'Not set'}\n\n""Press ENTER to change.",
            "on_select": root_password.set_root_password,
            "children":  [],
        },
        {
            "label":     "Features",
            "info":      lambda: f"""Current virtual ram: {configuration_config._config['features']['virtual_ram']}
                                     Current nvidia status: {configuration_config._config['features']['nvidia']}
                                     Current waydroid status: {configuration_config._config['features']['waydroid']}
                                     Current flatpak status: {configuration_config._config['features']['flatpak']}

                                     Press ENTER to configure the features.""",
            "on_select": None,
            "children":  [
                        {
                            "label":     "Choose virtual ram",
                            "info":      lambda: f"Current virtual ram option: {configuration_config._config['features']['virtual_ram']}\n\nPress Enter to choose virtual ram.",
                            "on_select": virtual_ram.choose_virtual_ram_options,
                            "children":  [],
                        },
                        {
                            "label":     "Configuration nvidia",
                            "info":      lambda: f"Current nvidia status: {configuration_config._config['features']['nvidia']}\n\nPress Enter to configuration nvidia.",
                            "on_select": nvidia.choose_nvidia_options,
                            "children":  [],
                        },
                        {
                            "label":     "Configuration waydroid",
                            "info":      lambda: f"Current waydroid status: {configuration_config._config['features']['waydroid']}\n\nPress Enter to configuration nvidia.",
                            "on_select": waydroid.choose_waydroid_options,
                            "children":  [],
                        },
                        {
                            "label":     "Configuration flatpak",
                            "info":      lambda: f"Current flatpak status: {configuration_config._config['features']['flatpak']}\n\nPress Enter to configuration nvidia.",
                            "on_select": flatpak.choose_flatpak_options,
                            "children":  [],
                        },
            ], 
        },
        {
            "label":     "-----------------------------",
            "info":      "Just a separator lol xD",
            "on_select": None,
            "children":  [],
        },
        {
            "label":     "Run the installer",
            "info":      "Make sure you have configured everything correctly before running the installer!",
            "on_select": run_installer,
            "children":  [],
        },
        {
            "label":     "Save configuration as toml file",
            "info":      "Save your configuration as a toml file.",
            "on_select": run_installer,
            "children":  [],
        },
        {
            "label":     "Exit",
            "info":      "Exit the installer.",
            "on_select": exit_installer,
            "children":  [],
        },
    ]
    drawer.run_menu(menu, title="RengeOS - Immutable OS Installer - Configuration")


if __name__ == "__main__":
    main()