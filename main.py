import os
from tools import installer, build_slot
from rich import print
from rich.prompt import Prompt, Confirm

def main():
    os.system('clear')
    print("[bold green]Welcome to Immutable RengeOS Tools![/bold green]")
    print("[bold cyan]Select your options:[/bold cyan]")
    print("1. Start installer")
    print("2. Build a new slot")
    print("3. Exit")
    choice = Prompt.ask("Select", choices=["1", "2", "3"])

    if choice == "1":
        confirm = Confirm.ask("Are you sure to run installer?")
        if confirm:
            print("[green]Starting installer...[/green]")
            try:
                installer.main()
            except:
                print("Unknown error with option 1 in installer.py file!")
        else:
            print("[yellow]Cancelled[/yellow]")

    elif choice == "2":
        confirm = Confirm.ask("Are you sure to build a new slot?")
        if confirm:
            print("[green]Starting tools[/green]...")
            try:
                build_slot.main()
            except:
                print("Unknown error with option 2 installer.py file!")

        else:
            print("[yellow]Cancelled[/yellow]")

    elif choice == "3":
        print("Have a good day!")
        return 0

# Init main function
if __name__ == "__main__":
    main()