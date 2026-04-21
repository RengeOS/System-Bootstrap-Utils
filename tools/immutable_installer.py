import os
import re
from getpass import getpass
import subprocess
from .modules import (
get_information, drawer, system_locale, hostname, timezone, root_password,
user_account, virtual_ram, immutable_os_config, nvidia, waydroid,
flatpak, disk, bluetooth, power_management, profile, audio,
slot_a_b, chroot, systemd_service, arch_package_manager
)
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
            "info":      lambda: f"Current hostname: {immutable_os_config._config["system"]["hostname"]}\n\nPress ENTER to change.",
            "on_select": hostname.set_hostname,
            "children":  [],
        },
        {
            "label":     "Timezone and System Locale",
            "info":      lambda: f"""Current timezone: {immutable_os_config._config["system"]['timezone']}
                                     Current system locale: {immutable_os_config._config["system"]["system_locale"]}
                                  
                                  Press Enter to configuration the timezone and system locale.""",
            "on_select": None,
            "children": [
                        {
                            "label":     "Timezone",
                            "info":      lambda: f"Current timezone: {immutable_os_config._config["system"]["timezone"]}\n\nPress ENTER to change timezone.",
                            "on_select": timezone.set_timezone,
                            "children":  [],
                        },
                        {
                            "label":     "System Locale",
                            "info":      lambda: f"Current system locale: {immutable_os_config._config["system"]["system_locale"]}\n\nPress ENTER to change system locale.",
                            "on_select": system_locale.set_locale,
                            "children":  [],
                        },
            ],
        },
        {
            "label":     "Disk",
            "info":      lambda: f"""Press Enter to configuration disk.
            
                                     Partitions status:

                                     + EFI partition: {immutable_os_config._config["disk"]["layout"]["efi_partition"]}
                                     + Data partition: {immutable_os_config._config["disk"]["layout"]["data_partition"]}
                                     + Repair partition: {immutable_os_config._config["disk"]["layout"]["repair_partition"]}
                                     + Boot_A partition: {immutable_os_config._config["disk"]["layout"]["boot_a_partition"]}
                                     + Boot_B partition: {immutable_os_config._config["disk"]["layout"]["boot_b_partition"]}
                                     + Root_A partition: {immutable_os_config._config["disk"]["layout"]["root_a_partition"]}
                                     + Root_B partition: {immutable_os_config._config["disk"]["layout"]["root_b_partition"]}
                                     + Swap partition: {immutable_os_config._config["disk"]["layout"]["swap_partition"]}

                                     Disk info:

                                     {disk.show_disk_info()}""",
            "on_select": None,
            "children":  [
                        {
                            "label":     "Edit disk",
                            "info":      lambda: f"""Press Enter to configuration disk.

                                                  Disk info:

                                                  {disk.show_disk_info()}""",
                            "on_select": disk.edit_disk,
                            "children":  [],
                        },
                        {
                            "label":     "Select EFI partition",
                            "info":      lambda: f"Current EFI partition: {immutable_os_config._config["disk"]["layout"]["efi_partition"]}\n\nPress ENTER to change efi partition.",
                            "on_select": disk.choose_efi_partition,
                            "children":  [],
                        },
                        {
                            "label":     "Select Data partition",
                            "info":      lambda: f"Current Data partition: {immutable_os_config._config["disk"]["layout"]["data_partition"]}\n\nPress ENTER to change data partition.",
                            "on_select": disk.choose_data_partition,
                            "children":  [],
                        },
                        {
                            "label":     "Select Repair partition",
                            "info":      lambda: f"Current Repair partition: {immutable_os_config._config["disk"]["layout"]["repair_partition"]}\n\nPress ENTER to change repair partition.",
                            "on_select": disk.choose_repair_partition,
                            "children":  [],
                        },
                        {
                            "label":     "Select Boot_A partition",
                            "info":      lambda: f"Current Boot_A partition: {immutable_os_config._config["disk"]["layout"]["boot_a_partition"]}\n\nPress ENTER to change boot_a partition.",
                            "on_select": disk.choose_boot_a_partition,
                            "children":  [],
                        },
                        {
                            "label":     "Select Boot_B partition",
                            "info":      lambda: f"Current Boot_B partition: {immutable_os_config._config["disk"]["layout"]["boot_b_partition"]}\n\nPress ENTER to change boot_b partition.",
                            "on_select": disk.choose_boot_b_partition,
                            "children":  [],
                        },
                        {
                            "label":     "Select Root_A partition",
                            "info":      lambda: f"Current Root_A partition: {immutable_os_config._config["disk"]["layout"]["root_a_partition"]}\n\nPress ENTER to change root_a partition.",
                            "on_select": disk.choose_root_a_partition,
                            "children":  [],
                        },
                        {
                            "label":     "Select Root_B partition",
                            "info":      lambda: f"Current Root_B partition: {immutable_os_config._config["disk"]["layout"]["root_b_partition"]}\n\nPress ENTER to change root_b partition.",
                            "on_select": disk.choose_root_b_partition,
                            "children":  [],
                        },
                        {
                            "label":     "Select Swap partition",
                            "info":      lambda: f"Current Swap partition: {immutable_os_config._config["disk"]["layout"]["swap_partition"]}\n\nPress ENTER to change swap partition.",
                            "on_select": disk.choose_swap_partition,
                            "children":  [],
                        },

            ],
        },
        {
            "label":     "User account",
            "info":      lambda: f"{user_account.user_account_status()}\n\nPress Enter to configuration user account.",
            "on_select": None,
            "children":  [
                        {
                            "label":     "Add user account",
                            "info":      lambda: f"{user_account.user_account_status()}\n\nPress Enter to add user account.",
                            "on_select": user_account.add_user,
                            "children":  [],
                        },
                        {
                            "label":     "Configuration user account",
                            "info":      lambda: f"{user_account.user_account_status()}\n\nPress Enter to configuration user account.",
                            "on_select": user_account.configure_user,
                            "children":  [],
                        },
            ],    
        },
        {
            "label":     "Root password",
            "info":      lambda: f"Root password hash: " f"{immutable_os_config._config["accounts"]["root"]["password"]}\n\n""Press ENTER to change root password.",
            "on_select": root_password.set_root_password,
            "children":  [],
        },
        {
            "label":     "Profile",
            "info":      lambda: f"Current profile: {immutable_os_config._config["system"]["profile"]}\n\n""Press ENTER to change profile.",
            "on_select": profile.choose_profile_options,
            "children":  [],
        },
        {
            "label":     "Audio",
            "info":      lambda: f"Current audio: {immutable_os_config._config["system"]["audio"]}\n\nPress Enter to change audio.",
            "on_select": audio.choose_audio_options,
            "children":  [],
        },
        {
            "label":     "Next slot",
            "info":      lambda: f"""Current next slot: {immutable_os_config._config["deployment"]["next_slot"]}
                                    
                                    The next slot is where you define the slot to build from. If you don't have any slots yet, choose Slot A or Slot B to build with and use.
                                    
                                    Press Enter to change next slot.""",
            "on_select": slot_a_b.choose_next_slot_options,
            "children":  [],
        },
        {
            "label":     "Packages",
            "info":      lambda: f"""Current packages: {immutable_os_config._config["packages"]["list_packages"]}
                                     Current AUR packages: {immutable_os_config._config["packages"]["list_aur_packages"]}
                                     
                                     Press Enter to edit packages list.""",
            "on_select": arch_package_manager.edit_packages,
            "children":  [],
        },
        {
            "label":     "Services",
            "info":      lambda: f"""Current enabled services: {immutable_os_config._config["services"]["list_enabled_services"]}
                                     Current disabled services: {immutable_os_config._config["services"]["list_disabled_services"]}
                                     
                                     Press Enter to edit commands in chroot.""",
            "on_select": systemd_service.edit_systemd_services,
            "children":  [],
        },
        {
            "label":     "Commands in chroot",
            "info":      lambda: f"Current commands: {immutable_os_config._config["commands_in_chroot"]["list_commands"]}\n\nPress Enter to edit commands in chroot.",
            "on_select": chroot.edit_commands_in_chroot,
            "children":  [],
        },
        {
            "label":     "Features",
            "info":      lambda: f"""Current virtual ram: {immutable_os_config._config['features']['virtual_ram']}
                                     Current nvidia status: {immutable_os_config._config['features']['nvidia']}
                                     Current waydroid status: {immutable_os_config._config['features']['waydroid']}
                                     Current flatpak status: {immutable_os_config._config['features']['flatpak']}
                                     Current bluetooth status: {immutable_os_config._config['features']['bluetooth']}
                                     Current power management: {immutable_os_config._config['features']['power_management']}

                                     Press ENTER to configure the features.""",
            "on_select": None,
            "children":  [
                        {
                            "label":     "Configuration virtual ram",
                            "info":      lambda: f"Current virtual ram option: {immutable_os_config._config['features']['virtual_ram']}\n\nPress Enter to configuration virtual ram.",
                            "on_select": virtual_ram.choose_virtual_ram_options,
                            "children":  [],
                        },
                        {
                            "label":     "Configuration nvidia",
                            "info":      lambda: f"Current nvidia status: {immutable_os_config._config['features']['nvidia']}\n\nPress Enter to configuration nvidia.",
                            "on_select": nvidia.choose_nvidia_options,
                            "children":  [],
                        },
                        {
                            "label":     "Configuration waydroid",
                            "info":      lambda: f"Current waydroid status: {immutable_os_config._config['features']['waydroid']}\n\nPress Enter to configuration nvidia.",
                            "on_select": waydroid.choose_waydroid_options,
                            "children":  [],
                        },
                        {
                            "label":     "Configuration flatpak",
                            "info":      lambda: f"Current flatpak status: {immutable_os_config._config['features']['flatpak']}\n\nPress Enter to configuration nvidia.",
                            "on_select": flatpak.choose_flatpak_options,
                            "children":  [],
                        },
                        {
                            "label":     "Configuration bluetooth",
                            "info":      lambda: f"Current bluetooth status: {immutable_os_config._config['features']['bluetooth']}\n\nPress Enter to configuration bluetooth.",
                            "on_select": bluetooth.choose_bluetooth_options,
                            "children":  [],
                        },
                        {
                            "label":     "Configuration power management",
                            "info":      lambda: f"Current power management: {immutable_os_config._config['features']['power_management']}\n\nPress Enter to configuration power management.",
                            "on_select": power_management.choose_power_management_options,
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
            "label":     "Save configuration as TOML file",
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