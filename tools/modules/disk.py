import os
import subprocess
import json
from . import immutable_os_config
from rich import print
from rich.prompt import Confirm

# This function retrieves the disk name of the computer, such as "/dev/sda" or "/dev/nvme0n1" and return it as a list python
def get_disks_list():
    cmd = ["lsblk", "-dn", "-o", "NAME,TYPE"]
    output = subprocess.check_output(cmd, text=True)
    disks = []
    for line in output.strip().split("\n"):
        name, typ = line.split()
        if typ == "disk":
            disks.append(f"/dev/{name}")
    return disks

def get_partitions_list():
    cmd = ["lsblk", "-ln", "-o", "NAME,TYPE"]
    output = subprocess.check_output(cmd, text=True)
    partitions = []
    for line in output.strip().split("\n"):
        parts = line.split()

        # Skip malformed lines
        if len(parts) < 2:
            continue

        name, typ = parts[0], parts[1]

        # Only collect partitions, skip disks and other types
        if typ == "part":
            partitions.append(f"/dev/{name}")

    return partitions


def configuration_disk():
    os.system("clear")
    print(
        "[yellow]Before editing the hard drive[/yellow], we need to acknowledge that any operation you perform "
        "in [red]cfdisk*[/red] on a hard drive partition can affect the data on that partition, and it could be "
        "lost at any time due to careless actions you take!"
    )
    confirm = Confirm.ask("So, have you accepted the confirmation and are you ready to proceed?")

    if not confirm:
        return

    os.system("clear")
    print("""Here I will show you a sample of how to partition a hard drive for Immutable OS, and this is required!
            | Our partitioning will be as follows:
            v
            - /dev/sda:    [Partition]         [Min]        [Max]                     [Recommend]
            + /dev/sda1 -> efi_partition    ->  Min: 512MB, Max: 1GB,                 Recommend: 512MB 
            + /dev/sda2 -> boot_a_partition ->  Min: 512MB, Max: As much as you like, Recommend: 1GB
            + /dev/sda3 -> boot_b_partition ->  Min: 512MB, Max: As much as you like, Recommend: 1GB
            + /dev/sda4 -> root_a_partition ->  Min: 20GB,  Max: As much as you like, Recommend: 20GB
            + /dev/sda5 -> root_b_partition ->  Min: 20GB,  Max: As much as you like, Recommend: 20GB
            + /dev/sda6 -> data_partition   ->  Min: 10GB,  Max: As much as you like, Recommend: 40GB
            + /dev/sda7 -> repair_partition ->  Min: 5GB,   Max: As much as you like, Recommend: 7GB
        """)
    print("[yellow bold]If you understand[/yellow bold], then select the hard drive you want to modify :D")

    _disk_options = get_disks_list()

    while True:
        print("\nOptions:")
        print("0. [red bold]Exit[/red bold]")
        for i, opt in enumerate(_disk_options, 1):
            print(f"{i}. {opt}")

        choice = input("\nEnter option (number or text): ").strip().lower()

        # Exit option
        if choice == "0" or choice == "exit":
            print("Exiting...")
            return

        # Number select
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(_disk_options):
                os.system(f"cfdisk {_disk_options[idx]}")
                return
            else:
                print("[red]Invalid choice! Please enter a valid number.[/red]")
                continue

        # Text select
        matched = False
        for opt in _disk_options:
            if choice == opt.lower():
                os.system(f"cfdisk {opt}")
                return
            else:
                print("[red]Invalid choice! Try again.[/red]")

def show_disk_info():

    def run(*cmd):
        # Run a shell command, return stdout or empty string on failure
        try:
            return subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True)
        except Exception:
            return ""

    def val(x):
        # Return x if it has a real value, otherwise "Unknown"
        return x if x and str(x).strip() else "Unknown"

    def interface(tran, rota, dtype):
        # Convert lsblk transport/rotation fields into a readable interface name
        tran = (tran or "").upper()
        if dtype == "loop":         return "Loop (virtual)"
        if dtype == "rom":          return "Optical / ROM"
        if tran == "NVME":          return "NVMe SSD"
        if tran in ("USB", "USB3"): return "USB"
        if tran in ("SATA", "ATA"): return "HDD" if rota else "SSD"
        if tran == "MMC":           return "eMMC / SD Card"
        if rota == 0:               return "SSD"
        if rota == 1:               return "HDD"
        return "Unknown"

    # Fetch block device tree as JSON
    lsblk_out = run("lsblk", "-J", "-o", "NAME,SIZE,FSTYPE,TRAN,TYPE,MOUNTPOINTS,ROTA")

    # Fetch used space in GB per device from df (df -h gives human-readable sizes)
    df_map = {}
    for line in run("df", "-BG", "--output=source,used").splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 2:
            name = parts[0].split("/")[-1]
            # strip trailing "G" to keep just the number, e.g. "12G" → "12G"
            df_map[name] = parts[1]

    # Column header labels
    COL_CAP  = "[Capacity]"
    COL_USED = "[Used]"
    COL_FMT  = "[Format]"
    COL_TYPE = "[Type Disk]"

    lines = []

    def format_disk(disk):
        disk_name = disk.get("name", "?")
        disk_tran = disk.get("tran") or ""
        disk_rota = disk.get("rota")
        children  = disk.get("children") or []

        # Collect partition data
        parts = []
        for child in children:
            cname = child.get("name", "?")
            ctran = child.get("tran") or disk_tran
            crota = child.get("rota") if child.get("rota") is not None else disk_rota
            parts.append({
                "name":  cname,
                "cap":   val(child.get("size")),
                "used":  val(df_map.get(cname)),    # GB used from df
                "fmt":   val(child.get("fstype")),
                "iface": interface(ctran, crota, "part"),
            })

        # Disk header line
        lines.append(
            f"- /dev/{disk_name}:  "
            f"{COL_CAP} | {COL_USED} | {COL_FMT} | {COL_TYPE}"
        )
        lines.append("")

        # One line per partition
        for p in parts:
            lines.append(
                f"  + {p['name']}  "
                f"{p['cap']} | "
                f"{p['used']} | "
                f"{p['fmt']} | "
                f"{p['iface']}"
            )

        lines.append("")
        lines.append("")

    try:
        devices = json.loads(lsblk_out).get("blockdevices", [])
        for device in devices:
            if device.get("type") == "disk":
                format_disk(device)
    except Exception:
        lines.append("lsblk not available or not running on Linux")

    return "\n".join(lines).rstrip()

def choose_efi_partition():
    _partition_options = get_partitions_list()
    os.system("clear")
    while True:
        print("\nAvailable partition:")
        for i, opt in enumerate(_partition_options, 1):
            print(f"{i}. {opt}")

        choice = input("\nEnter option (name or number): ").strip().lower()

        # Select with number
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(_partition_options):
                immutable_os_config._config["disk"]["layout"]["efi_partition"] = _partition_options[idx]
                break

        # Select with text
        for opt in _partition_options:
            if choice == opt.lower():
                immutable_os_config._config["disk"]["layout"]["efi_partition"] = opt
                return

        print("Invalid choice! Please try again.")

def choose_data_partition():
    _partition_options = get_partitions_list()
    os.system("clear")
    while True:
        print("\nAvailable partition:")
        for i, opt in enumerate(_partition_options, 1):
            print(f"{i}. {opt}")

        choice = input("\nEnter option (name or number): ").strip().lower()

        # Select with number
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(_partition_options):
                immutable_os_config._config["disk"]["layout"]["data_partition"] = _partition_options[idx]
                break

        # Select with text
        for opt in _partition_options:
            if choice == opt.lower():
                immutable_os_config._config["disk"]["layout"]["data_partition"] = opt
                return

        print("Invalid choice! Please try again.")

def choose_repair_partition():
    _partition_options = get_partitions_list()
    os.system("clear")
    while True:
        print("\nAvailable partition:")
        for i, opt in enumerate(_partition_options, 1):
            print(f"{i}. {opt}")

        choice = input("\nEnter option (name or number): ").strip().lower()

        # Select with number
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(_partition_options):
                immutable_os_config._config["disk"]["layout"]["repair_partition"] = _partition_options[idx]
                break

        # Select with text
        for opt in _partition_options:
            if choice == opt.lower():
                immutable_os_config._config["disk"]["layout"]["repair_partition"] = opt
                return

        print("Invalid choice! Please try again.")