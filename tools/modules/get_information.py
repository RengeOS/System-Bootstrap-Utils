import os
import subprocess

def get_boot_mode_information():
    if os.path.exists("/sys/firmware/efi/efivars"):
        boot_mode = "UEFI"
        boot_filesystem_supported = ["vfat, ""xfs", "ext4", "btrfs"]
    else:
        boot_mode = "LEGACY"
        boot_filesystem_supported = ["xfs", "ext4", "btrfs"]
    return boot_mode, boot_filesystem_supported

def get_cpu_information():
    cmd = ["lscpu | grep 'Model name' | cut -d ':' -f2 | xargs"]
    cpu_result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    # Use a strip to remove the \n from the output.
    return cpu_result.stdout.strip()

def get_gpu_information():
    cmd = ["lspci | grep -iE 'vga|3d' | awk -F'[][]' '{print $(NF-1)}'"]
    gpu_result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    # Use splitlines to get list of gpu
    return gpu_result.stdout.splitlines()

def get_model_information():
    cmd = ["cat /sys/class/dmi/id/product_version"]
    model_result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return model_result.stdout.strip()

def get_vendor_model_information():
    cmd = ["cat /sys/class/dmi/id/sys_vendor"]
    vendor_model_result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return vendor_model_result.stdout.strip()