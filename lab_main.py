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

# Пример использования:
disk_space = get_disk_space()
for disk, usage in disk_space.items():
    print(f"Диск {disk}:")
    print(f"  Всего: {usage['total']:.2f} ГБ")
    print(f"  Использовано: {usage['used']:.2f} ГБ")
    print(f"  Свободно: {usage['free']:.2f} ГБ")
    print(f"  Использовано: {usage['percent']}%")


def get_swap_size():
    swap = psutil.swap_memory()
    return {
        'total': swap.total / (1024 ** 3),
        'used': swap.used / (1024 ** 3),
        'free': swap.free / (1024 ** 3),
        'percent': swap.percent
    }

# Пример использования:
swap_info = get_swap_size()
print(f"Размер свап файла:")
print(f"  Всего: {swap_info['total']:.2f} ГБ")
print(f"  Использовано: {swap_info['used']:.2f} ГБ")
print(f"  Свободно: {swap_info['free']:.2f} ГБ")
print(f"  Использовано: {swap_info['percent']}%")
