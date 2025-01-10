import sys
import time
import psutil
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QPushButton

from database import Database
from interface import create_monitor_layout, create_history_window

class SystemMonitorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Системный монитор")
        self.setGeometry(100, 100, 400, 300)

        # Переменные
        self.timer = QTimer()  # Таймер для записи данных
        self.display_timer = QTimer()  # Таймер для обновления времени записи
        self.recording = False
        self.start_time = None
        self.db_connection = Database()
        self.db_connection.connect_to_db()


        # Интерфейс
        self.layout = create_monitor_layout(self)
        self.setLayout(self.layout)

        self.start_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)
        self.view_history_button.clicked.connect(self.view_history)
        self.stop_button.hide()  # Скрываем, пока запись не начата

        # Таймеры
        self.timer.timeout.connect(self.update_stats)
        self.display_timer.timeout.connect(self.update_timer)



    def update_stats(self):
        # Получаем данные о системе
        cpu = psutil.cpu_percent()

        # ОЗУ
        ram_info = psutil.virtual_memory()
        ram_available = ram_info.available / (1024 ** 3)  # Свободно в ГБ
        ram_total = ram_info.total / (1024 ** 3)  # Всего в ГБ

        # ПЗУ
        disk_info = psutil.disk_usage('/')
        disk_free = disk_info.free / (1024 ** 3)  # Свободно в ГБ
        disk_total = disk_info.total / (1024 ** 3)  # Всего в ГБ

        # Обновляем метки
        self.cpu_label.setText(f"CPU: {cpu}%")
        self.ram_label.setText(f"RAM: {ram_available:.2f}/{ram_total:.2f} GB")
        self.disk_label.setText(f"Disk: {disk_free:.2f}/{disk_total:.2f} GB")

        # Если идет запись, сохраняем данные в БД
        if self.recording:
            self.db_connection.save_to_db(cpu, ram_available, ram_total, disk_total, disk_free)

    def start_recording(self):
        try:
            interval = int(self.interval_input.text())
            if interval < 1:
                raise ValueError("Интервал должен быть не менее 1 секунды.")

            self.start_time = time.time()
            self.recording = True
            self.start_button.hide()
            self.stop_button.show()

            # Сразу обновляем данные
            self.update_stats()

            # Запускаем таймеры
            self.timer.start(interval * 1000)  # Таймер для записи данных
            self.display_timer.start(1000)  # Таймер для обновления времени записи
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", f"Некорректный интервал: {e}")

    def view_history(self):
        try:
            data = self.db_connection.fetch_all_records()  # Получаем данные из базы
            create_history_window(data)  # Создаем и показываем окно истории
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные истории: {e}")

    def stop_recording(self):
        self.recording = False
        self.start_time = None

        self.timer_label.setText("Время записи: 0 секунд")
        self.cpu_label.setText(f"CPU: 0%")
        self.ram_label.setText(f"RAM: 0/0 GB")
        self.disk_label.setText(f"Disk: 0/0 GB")

        self.stop_button.hide()
        self.start_button.show()

        if self.timer.isActive():
            self.timer.stop()  # Останавливаем таймер записи данных
        if self.display_timer.isActive():
            self.display_timer.stop()  # Останавливаем таймер отображения времени

    def update_timer(self):
        if self.recording and self.start_time:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.setText(f"Время записи: {format_seconds(elapsed)}")

    def closeEvent(self, event):
        # Закрытие соединения с базой данных
        if self.db_connection:
            self.db_connection.close()
        event.accept()


def format_seconds(seconds):
    if 11 <= seconds % 100 <= 19:
        return f"{seconds} секунд"
    last_digit = seconds % 10
    if last_digit == 1:
        return f"{seconds} секунда"
    elif 2 <= last_digit <= 4:
        return f"{seconds} секунды"
    else:
        return f"{seconds} секунд"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    monitor_app = SystemMonitorApp()
    monitor_app.show()
    sys.exit(app.exec_())
