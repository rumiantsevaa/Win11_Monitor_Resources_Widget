import psutil
import GPUtil
import win32gui
import win32process
import wmi
import os
import subprocess
import ctypes
from datetime import date
import time
from path import HWM_PATH, HWM_LOG_PATH


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except ValueError:
        return False


def run_openhardwaremonitor():
    openhardwaremonitor_path = HWM_PATH
    if not os.path.exists(openhardwaremonitor_path):
        raise FileNotFoundError(f"{openhardwaremonitor_path} not found.")

    if is_admin():
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        time.sleep(0.5)
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.name() == "OpenHardwareMonitor.exe":
                proc.terminate()
    else:
        params = ' '.join([openhardwaremonitor_path])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", "python", params, None, 1)


def get_cpu_temp():
    run_openhardwaremonitor()
    now = date.today()
    infile = HWM_LOG_PATH + now.strftime("%Y-%m-%d") + ".csv"

    if not os.path.exists(infile):
        raise FileNotFoundError(f"{infile} not found.")

    with open(infile, "r") as f:
        last_line = f.readlines()[-1]
        output = last_line.split(',')
        print(output)
        cpu_temp = output[9]
        return cpu_temp


def get_gpu_temp():
    gpus = GPUtil.getGPUs()
    if not gpus:
        return None
    gpu_temps = [gpu.temperature for gpu in gpus]
    return gpu_temps


def get_active_window_process_name():
    try:
        pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())[1]
        process_name = psutil.Process(pid).name()
        return process_name
    except:
        return None


def get_disk_usage():
    disk_usages = {}
    partitions = psutil.disk_partitions()
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        disk_usages[partition.device] = {
            'total': usage.total,
            'used': usage.used,
            'free': usage.free,
            'percent': usage.percent
        }
    return disk_usages


def get_system_info():
    cpu_percent = psutil.cpu_percent(interval=5)

    gpus = GPUtil.getGPUs()
    gpu_percent = gpus[0].load * 100 if gpus else None
    gpu_memory_percent = gpus[0].memoryUsed / gpus[0].memoryTotal * 100 if gpus else None
    ram = psutil.virtual_memory()
    ram_percent = ram.percent
    disk_usage = get_disk_usage()

    active_process = get_active_window_process_name()
    fps = "N/A"
    if active_process:
        c = wmi.WMI()
        for process in c.Win32_PerfFormattedData_PerfProc_Process(Name=active_process):
            fps = process.ElapsedTime
            break

    return {
        "cpu_percent": cpu_percent,
        "gpu_percent": gpu_percent,
        "gpu_memory_percent": gpu_memory_percent,
        "ram_percent": ram_percent,
        "fps": fps,
        "disk_usage": disk_usage
    }


if __name__ == "__main__":
    if is_admin():

        cpu_temp = get_cpu_temp()
        print(f"CPU Temperature: {cpu_temp}" + "°C")

        gpu_temps = get_gpu_temp()
        if gpu_temps:
            for i, temp in enumerate(gpu_temps):
                print(f"GPU {i} Temperature: {temp}°C")
        else:
            print("No GPUs found.")

        system_info = get_system_info()
        print(f"CPU load: {system_info['cpu_percent']:.1f}%")

        if system_info['gpu_percent'] is not None:
            print(f"GPU load: {system_info['gpu_percent']:.1f}%")
        else:
            print("GPU load: N/A")
        if system_info['gpu_memory_percent'] is not None:
            print(f"Videomemory load: {system_info['gpu_memory_percent']:.1f}%")
        else:
            print("Videomemory load: N/A")
        print(f"RAM load: {system_info['ram_percent']:.1f}%")
        print(f"FPS: {system_info['fps']}")

        for disk, usage in system_info['disk_usage'].items():
            print(f"Disk {disk}:")
            print(f"  Total: {usage['total'] / (1024 ** 3):.2f} GB")
            print(f"  Used: {usage['used'] / (1024 ** 3):.2f} GB")
            print(f"  Free: {usage['free'] / (1024 ** 3):.2f} GB")
            print(f"  Usage: {usage['percent']}%")
    else:
        print("Please run the script as administrator.")
