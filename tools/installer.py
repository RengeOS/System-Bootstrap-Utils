import os
from . import mutable_installer, immutable_installer
from rich import print
from rich.prompt import Prompt, Confirm

def main():
    os.system('sleep 0.5')
    os.system('clear')
    print("[bold green]Hey! Before starting the installer, please choose your installation method:D[/bold green]")
    print("[bold cyan]Select your options:[/bold cyan]")
    print("1. [blue bold]Immutable OS[/blue bold] Installer")
    print("2. [blue bold]Mutable OS[/blue bold] Installer")
    print("3. [bold red]Exit[/bold red]")
    choice = Prompt.ask("Select", choices=["1", "2", "3"])

    if choice == "1":
        confirm = Confirm.ask("[yellow bold]Are you sure[/yellow bold] to [red bold]install immutable system[/red bold]?")
        if confirm:
            print("[green]Running installer[/green]...")
            try:
                immutable_installer.main()
            except Exception as e:
                print(f"Unknown error: {e}")
        else:
            print("\n[yellow bold]Cancelled[/yellow bold]")

    elif choice == "2":
        confirm = Confirm.ask("[yellow bold]Are you sure[yellow bold] to [red bold]install mutable system[/red bold]?")
        if confirm:
            print("[green]Running installer...[/green]")
            try:
                mutable_installer.main()
            except Exception as e:
                print(f"Unknown error: {e}")
        else:
            print("[yellow]Cancelled[/yellow]")

    elif choice == "3":
        print("\n[magenta3 bold]Have a good day![/magenta3 bold]")
        raise SystemExit(0)

if __name__ == "__main__":
    main()