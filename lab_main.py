import psutil

def get_disk_space():
    disk_usage = {}
    partitions = psutil.disk_partitions()
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        disk_usage[partition.device] = {
            'total': usage.total / (1024 ** 3),
            'used': usage.used / (1024 ** 3),
            'free': usage.free / (1024 ** 3),
            'percent': usage.percent
        }
    return disk_usage
