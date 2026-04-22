from rich import print
from . import immutable_os_config
import tomllib, toml
import os

path_configuration = [
    "/var/lib/system-bootstrap-utils/configuration.toml",
    # os.path.expanduser("~/.config/system-bootstrap-utils/configuration.toml")
]

def validate_configuration(path):
    found_any = False
    data = {}

    for config_path in path:
        if not os.path.exists(config_path):
            print(f"[red bold]| {config_path} not found |[/red bold]")
            continue

        found_any = True
        print(f"[green bold]| {config_path} found! |[/green bold]")

        with open(config_path, "rb") as f:
            try:
                data.update(tomllib.load(f))
            except tomllib.TOMLDecodeError as e:
                print(f"[red bold]Error:[/red bold] [red]{e}[/red]")
            except Exception as e:
                print(f"[red bold]Unexpected error:[/red bold] [red]{e}[/red]")

    if not found_any:
        print("[red bold]Error:[/red bold] [red]not found configuration.toml![/red]")
        return 0

    return data

def dump_config():

    os.system("clear")
    config = immutable_os_config._config

    print("Current config:")
    print(toml.dumps(config))

    choice = input("\nExport to /tmp/system-bootstrap-utils/configuration.toml? (y/n): ").strip().lower()
    if choice != "y":
        print("Cancelled.")
        input("Press Enter to continue...")
        return

    output_dir = "/tmp/system-bootstrap-utils"
    output_file = os.path.join(output_dir, "configuration.toml")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory '{output_dir}'.")

    with open(output_file, "w") as f:
        toml.dump(config, f)

    print(f"Config exported to '{output_file}'.")
    input("Press Enter to continue...")