import os
import subprocess

def get_boot_mode_information():
    if os.path.exists("/sys/firmware/efi/efivars"):
        boot_mode = "UEFI"
        boot_filesystem = ["vfat, ""xfs", "ext4", "btrfs"]
    else:
        boot_mode = ["LEGACY", "xfs"]
        boot_filesystem = ["xfs", "ext4", "btrfs"]
    return boot_mode, boot_filesystem

def get_cpu_information():
    cpu_result = subprocess.run(["lscpu | grep 'Model name' | cut -d ':' -f2 | xargs"],
    shell=True,
    capture_output=True,
    text=True)
    # Use a strip to remove the \n from the output.
    return cpu_result.stdout.strip()

def get_gpu_information():
    result = subprocess.run(["lspci | grep -iE 'vga|3d' | awk -F'[][]' '{print $(NF-1)}'"],
        shell=True,
        capture_output=True,
        text=True
    )
    # Use splitlines to get list of gpu
    return result.stdout.splitlines()

def get_model_information():
    result = subprocess.run(["cat /sys/class/dmi/id/product_version"],
    shell=True,
    capture_output=True,
    text=True)
    return result.stdout.strip()

def get_vendor_model_information():
    result = subprocess.run(["cat /sys/class/dmi/id/sys_vendor"],
    shell=True,
    capture_output=True,
    text=True)
    return result.stdout.strip()
# How to use:
"""
mode, fs = get_boot_mode()
print(mode)
print(fs)
"""