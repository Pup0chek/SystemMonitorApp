from PyQt5.QtWidgets import QApplication

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from interface import create_monitor_layout, create_history_window
import pytest

@pytest.fixture(scope="session")
def app():
    app = QApplication([])
    yield app
    app.quit()

def test_create_monitor_layout(qtbot):
    from PyQt5.QtWidgets import QWidget
    widget = QWidget()
    create_monitor_layout(widget)

    assert widget.cpu_label.text() == "CPU: 0%"
    assert widget.ram_label.text() == "RAM: 0/0 GB"
    assert widget.disk_label.text() == "Disk: 0/0 GB"

def test_create_history_window(qtbot):
    data = [
        (1, "2023-01-01 12:00:00", 50, 4.0, 8.0, 200.0, 100.0),
        (2, "2023-01-01 12:01:00", 60, 3.5, 8.0, 195.0, 100.0),
    ]
    create_history_window(data)
