import os
from .modules import get_information
from rich import print
from rich.prompt import Prompt, Confirm

def main():
    os.system("clear")
    boot_mode_info, boot_fs_info = get_information.get_boot_mode_information()
    model_info = get_information.get_model_information()
    vendor_model_info = get_information.get_vendor_model_information()
    cpu_info = get_information.get_cpu_information()
    gpu_info = get_information.get_gpu_information()

    print(f"[green bold]Hi! Welcome to the immutable RengeOS installer, yay![/green bold]")
    print("[cyan bold] - Some infomation about your system:[/cyan bold]")
    print(f"[purple] + Vendor:[/purple] {vendor_model_info}")
    print(f"[purple] + Model:[/purple] {model_info}")
    print(f"[purple] + CPU:[/purple] {cpu_info}")
    for gpu in gpu_info:
        print(f"[purple] + GPU:[/purple] {gpu}")
    print(f"[purple] + BIOS Mode:[/purple] {boot_mode_info}")

    confirm = Confirm.ask("[green bold]Now, let's begin the installation process, shall we?[/green bold]")
    if confirm:
        print("Let's go!")
    else:
        print("Have a good day!")
    
if __name__ == "__main__":
    main()