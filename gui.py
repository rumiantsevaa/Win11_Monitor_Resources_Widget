import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QSystemTrayIcon
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon
from main import is_admin, get_cpu_temp, get_gpu_temp, get_system_info


class SystemMonitorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.disk_update_counter = 0

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)

        layout = QGridLayout()
        self.info_label_left = QLabel()
        self.info_label_right = QLabel()

        style = "color: white; background-color: rgba(0, 0, 0, 180); padding: 10px; border-radius: 10px;"
        for label in (self.info_label_left, self.info_label_right):
            label.setStyleSheet(style)
            label.setMinimumWidth(200)  # Устанавливаем минимальную ширину для обоих блоков

        layout.addWidget(self.info_label_left, 0, 0)
        layout.addWidget(self.info_label_right, 0, 1)
        layout.setColumnStretch(0, 1)  # Устанавливаем одинаковое растяжение для обоих столбцов
        layout.setColumnStretch(1, 1)

        self.setLayout(layout)

        self.tray_icon = QSystemTrayIcon(QIcon("ico.ico"), self)
        self.tray_icon.show()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_info)
        self.timer.start(2000)

        self.update_info()
        self.show()

    def update_info(self):
        if not is_admin():
            self.info_label_left.setText("Please run the script as administrator.")
            self.info_label_right.clear()
            return

        try:
            cpu_temp = get_cpu_temp()
            gpu_temps = get_gpu_temp()
            system_info = get_system_info()

            left_text = []
            if gpu_temps:
                left_text.extend(f"GPU {i} Temp: {temp}°C" for i, temp in enumerate(gpu_temps))
                left_text.append(f"GPU Load: {system_info['gpu_percent']:.1f}%")
            else:
                left_text.append("No GPUs found.")

            left_text.extend([
                f"CPU Temp: {cpu_temp}°C",
                f"CPU Load: {system_info['cpu_percent']:.1f}%",
                f"RAM Load: {system_info['ram_percent']:.1f}%",
                f"FPS: {system_info['fps']}"
            ])

            self.info_label_left.setText('\n'.join(left_text))

            # Обновляем информацию о дисках каждые 10 секунд
            if self.disk_update_counter == 0:
                self.disk_info = []
                for disk, usage in system_info['disk_usage'].items():
                    self.disk_info.extend([
                        f"Disk {disk}:",
                        f"  Total: {usage['total'] / (1024 ** 3):.2f} GB",
                        f"  Free: {usage['free'] / (1024 ** 3):.2f} GB"
                    ])

            self.info_label_right.setText('\n'.join(self.disk_info))

            self.disk_update_counter = (self.disk_update_counter + 1) % 5  # 5 * 2 секунды = 10 секунд

        except Exception as e:
            self.info_label_left.setText(f"Error: {str(e)}")
            self.info_label_right.clear()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.drag_pos:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_pos = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = SystemMonitorWidget()
    sys.exit(app.exec_())