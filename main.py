import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox
import psutil
from PyQt5.QtCore import QTimer
import sqlite3


class SystemMonitorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Системный монитор")
        self.setGeometry(100, 100, 400, 300)

        self.timer = QTimer()  # для записи данных
        self.display_timer = QTimer()  # для обновления времени записи
        self.recording = False
        self.start_time = None
        self.db_connection = None

        # Интерфейс
        self.layout = QVBoxLayout()

        self.cpu_label = QLabel("CPU: 0%")
        self.layout.addWidget(self.cpu_label)

        self.ram_label = QLabel("RAM: 0/0 GB")
        self.layout.addWidget(self.ram_label)

        self.disk_label = QLabel("Disk: 0/0 GB")
        self.layout.addWidget(self.disk_label)

        self.interval_label = QLabel("Интервал обновления (с):")
        self.layout.addWidget(self.interval_label)

        self.interval_input = QLineEdit("1")
        self.layout.addWidget(self.interval_input)

        self.start_button = QPushButton("Начать запись")
        self.start_button.clicked.connect(self.start_recording)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Остановить")
        self.stop_button.clicked.connect(self.stop_recording)
        self.stop_button.hide()
        self.layout.addWidget(self.stop_button)

        self.timer_label = QLabel("Время записи: 0 секунд")
        self.layout.addWidget(self.timer_label)

        self.setLayout(self.layout)


        self.timer.timeout.connect(self.update_stats)
        self.display_timer.timeout.connect(self.update_timer)

    #подключение к бд
    def connect_to_db(self):
        try:
            self.db_connection = sqlite3.connect("system_monitor.db")
            cursor = self.db_connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS monitor_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    cpu_usage REAL,
                    ram_available REAL,
                    ram_total REAL,
                    disk_free REAL,
                    disk_total REAL
                )
            """)
            self.db_connection.commit()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка подключения", f"Не удалось подключиться к базе данных: {e}")
            sys.exit()

    def update_stats(self):
        #CPU
        cpu = psutil.cpu_percent()

        #ОЗУ
        ram_info = psutil.virtual_memory()
        ram_available = ram_info.available / (1024 ** 3)
        ram_total = ram_info.total / (1024 ** 3)

        #ПЗУ
        disk_info = psutil.disk_usage('/')
        disk_free = disk_info.free / (1024 ** 3)
        disk_total = disk_info.total / (1024 ** 3)


        self.cpu_label.setText(f"CPU: {cpu}%")
        self.ram_label.setText(f"RAM: {ram_available:.2f}/{ram_total:.2f} GB")
        self.disk_label.setText(f"Disk: {disk_free:.2f}/{disk_total:.2f} GB")

        #если запись идет, сохраняем данные в бд
        if self.recording:
            self.save_to_db(cpu, ram_available, ram_total, disk_free, disk_total)

    def save_to_db(self, cpu, ram_available, ram_total, disk_free, disk_total):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "INSERT INTO monitor_data (cpu_usage, ram_available, ram_total, disk_free, disk_total) VALUES (?, ?, ?, ?, ?)",
                (cpu, ram_available, ram_total, disk_free, disk_total)
            )
            self.db_connection.commit()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка записи", f"Не удалось записать данные: {e}")

    def start_recording(self):
        try:
            self.start_time = time.time()
            self.recording = True
            self.start_button.hide()
            self.stop_button.show()
            interval = int(self.interval_input.text())
            self.timer.start(interval * 1000)
            self.display_timer.start(1000)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Интервал должен быть числом.")

    def stop_recording(self):
        self.recording = False
        self.start_time = None
        self.timer_label.setText("Время записи: 0 секунд")
        self.stop_button.hide()
        self.start_button.show()
        self.timer.stop()
        self.display_timer.stop()

    def update_timer(self):
        if self.recording and self.start_time:
            sec = int(time.time() - self.start_time)
            self.timer_label.setText(f"Время записи: {sec}")

    def closeEvent(self, event):
        if self.db_connection:
            self.db_connection.close()
        event.accept()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    monitor_app = SystemMonitorApp()
    monitor_app.connect_to_db()
    monitor_app.show()
    sys.exit(app.exec_())
