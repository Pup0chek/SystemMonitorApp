from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QDialog


def create_monitor_layout(parent):
    layout = QVBoxLayout()

    parent.cpu_label = QLabel("CPU: 0%")
    layout.addWidget(parent.cpu_label)

    parent.ram_label = QLabel("RAM: 0/0 GB")
    layout.addWidget(parent.ram_label)

    parent.disk_label = QLabel("Disk: 0/0 GB")
    layout.addWidget(parent.disk_label)

    parent.interval_label = QLabel("Интервал обновления (с):")
    layout.addWidget(parent.interval_label)

    parent.interval_input = QLineEdit("1")
    layout.addWidget(parent.interval_input)

    parent.timer_label = QLabel("Время записи: 0 секунд")
    layout.addWidget(parent.timer_label)

    parent.start_button = QPushButton("Начать запись")
    layout.addWidget(parent.start_button)


    parent.stop_button = QPushButton("Остановить")
    parent.stop_button.hide()
    layout.addWidget(parent.stop_button)


    parent.view_history_button = QPushButton("Просмотреть историю")
    layout.addWidget(parent.view_history_button)

    return layout


def create_history_window(data):
    dialog = QDialog()
    dialog.setWindowTitle("История записей")
    dialog.setGeometry(100, 100, 1100, 500)
    table = QTableWidget(len(data), 6)
    table.setHorizontalHeaderLabels(
        ["ID", "Время", "CPU", "RAM (доступно)", "RAM (всего)", "Disk (свободно)", "Disk (всего)"])

    for row_idx, row_data in enumerate(data):
        for col_idx, value in enumerate(row_data):
            table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    layout = QVBoxLayout()
    layout.addWidget(table)
    dialog.setLayout(layout)
    dialog.exec_()

