import os
from tools import installer, build_slot
from tools.modules import get_information
from rich import print
from rich.prompt import Prompt, Confirm

def main():
    os.system('clear')
    print("[bold green]Welcome to System Bootstrap RengeOS Tools![/bold green]")
    print("[bold green]------------------------------------------[/bold green]")
    print("[yellow bold]>_Notes[/yellow bold]: [blue_violet]You might want to know more information about the device you're using:)[/blue_violet]")
    boot_mode_info, boot_fs_info = get_information.get_boot_mode_information()
    model_info = get_information.get_model_information()
    vendor_model_info = get_information.get_vendor_model_information()
    cpu_info = get_information.get_cpu_information()
    gpu_info = get_information.get_gpu_information()
    print("[yellow bold] - Some infomation about your system:[/yellow bold]")
    print(f"[purple] + Vendor:[/purple] {vendor_model_info}")
    print(f"[purple] + Model:[/purple] {model_info}")
    print(f"[purple] + CPU:[/purple] {cpu_info}")
    for gpu in gpu_info:
        print(f"[purple] + GPU:[/purple] {gpu}")
    print(f"[purple] + BIOS Mode:[/purple] {boot_mode_info}")

    print("[bold cyan]------------------------[/bold cyan]")
    print("[bold cyan]Now select your options:[/bold cyan]")
    print("1. [blue bold]Start[/blue bold] installer ([yellow]For Live ISO![/yellow])")
    print("2. [blue bold]Build[/blue bold] a new slot ([yellow]For Immutable OS![/yellow])")
    print("3. [blue bold]Reinstall[/blue bold] without usb ([yellow]For Mutable OS![/yellow])")
    print("4, [blue bold]Update[/blue bold] airootfs and kernels ([yellow]For Mutable OS![/yellow])")
    print("5. [red bold]Exit[/red bold]")
    choice = Prompt.ask("Select", choices=["1", "2", "3", "4", "5"])

    if choice == "1":
        confirm = Confirm.ask("[yellow bold]Are you sure[/yellow bold] to [red bold]run installer?[/red bold]")
        if confirm:
            print("[green]Starting installer...[/green]")
            try:
                installer.main()
            except Exception as e:
                print(f"Unknown error: {e}")
        else:
            print("[yellow]Cancelled[/yellow]")

    elif choice == "2":
        confirm = Confirm.ask("Are you sure to build a new slot?")
        if confirm:
            print("[green]Starting tools[/green]...")
            try:
                build_slot.main()
            except Exception as e:
                print(f"Unknown error: {e}")

        else:
            print("[yellow]Cancelled[/yellow]")

    elif choice == "3":
        print("\t[yellow bold]In developing![/yellow bold]")
        raise SystemExit(0)

    elif choice == "4":
        print("\t[yellow bold]In developing![/yellow bold]")
        raise SystemExit(0)
        
    elif choice == "5":
        print("\n[magenta3 bold]Ok! have a good day:D[/magenta3 bold]")
        raise SystemExit(0)

# Init main function
if __name__ == "__main__":
    main()