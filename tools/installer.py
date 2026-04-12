import os
from . import mutable_installer, immutable_installer
from rich import print
from rich.prompt import Prompt, Confirm

def main():
    os.system('sleep 0.5')
    os.system('clear')
    print("[bold green]Hey! Before starting the installer, please choose your installation method:D[/bold green]")
    print("[bold cyan]Select your options:[/bold cyan]")
    print("1. Mutable System Installer Method")
    print("2. Immutable System Installer Method")
    print("3. Exit")
    choice = Prompt.ask("Select", choices=["1", "2", "3"])

    if choice == "1":
        confirm = Confirm.ask("Are you sure to install mutable system?")
        if confirm:
            print("[green]Running installer...[/green]")
            try:
                mutable_installer.main()
            except:
                print("Unknown error!")
        else:
            print("[yellow]Cancelled[/yellow]")

    elif choice == "2":
        confirm = Confirm.ask("Are you sure to install immutable system?")
        if confirm:
            print("[green]Running installer[/green]...")
            try:
                immutable_installer.main()
            except:
                print("Unknown error!")
        else:
            print("[yellow]Cancelled[/yellow]")

    elif choice == "3":
        print("[green bold]Have a good day![/green bold]")
        return 0

if __name__ == "__main__":
    main()