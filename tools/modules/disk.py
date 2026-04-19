import os
import subprocess
import json
from . import configuration_config

_disk_method_option_list = ["Automatic"]


def choose_disk_method():
    os.system("clear")
    while True:
        print("\nAvailable options:")
        for i, opt in enumerate(_disk_method_option_list, 1):
            print(f"{i}. {opt}")

        choice = input("\nEnter option (name or number): ").strip().lower()

        # Select with number
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(_disk_method_option_list):
                configuration_config._config["disk"]["method"] = _disk_method_option_list[idx]
                break

        # Select with text
        for opt in _disk_method_option_list:
            if choice == opt.lower():
                configuration_config._config["disk"]["method"] = opt
                return

        print("Invalid choice! Please try again.")

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