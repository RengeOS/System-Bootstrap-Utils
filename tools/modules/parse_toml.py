from rich import print
import tomllib
import os

path_configuration = [
    "/var/lib/system-bootstrap-utils/configuration.toml",
    os.path.expanduser("~/.config/system-bootstrap-utils/configuration.toml")
]

# Used to check and read configurations
def validate_configuration(path):
    found_any_configuration = False
    data = {}
    for configuration in path:
        if os.path.exists(configuration):
            found_any_configuration = True
            print(f"[green bold]| {configuration} found! |[/green bold]")
            with open(configuration, "rb") as f:
                # Try load file configuration and see if it have an errors.
                try:
                    data.update(tomllib.load(f))
                except tomllib.TOMLDecodeError as e:
                    print(f"[red bold]Error:[/red bold] [red]{e}[/red]")
                except Exception as e:
                    print(f"[red bold]Unexpected error:[/red bold] [red]{e}[/red]")  
        else:
            print(f"[red bold]| {configuration} not found |[/red bold]")
    if not found_any_configuration:
        print("[red bold]Error:[/red bold] [red]not found configuration.toml![/red]")
        return 0

    return data

data_configuration = validate_configuration(path_configuration)