import os
import subprocess

# Check disks function.
def check_disks():
    result = subprocess.run(["lsblk", "-dn", "-o", "NAME"],
    shell=True,
    capture_output=True,
    text=True)
    return result.stdout.split()
