import pytest
from PyQt5.QtCore import Qt
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import SystemMonitorApp


def test_start_stop_recording(qtbot):
    from main import SystemMonitorApp

    monitor_app = SystemMonitorApp()
    qtbot.addWidget(monitor_app)

    # Интервал
    monitor_app.interval_input.setText("1")


    qtbot.mouseClick(monitor_app.start_button, Qt.LeftButton)
    assert monitor_app.recording is True
    assert monitor_app.timer.isActive()


    qtbot.mouseClick(monitor_app.stop_button, Qt.LeftButton)
    assert monitor_app.recording is False
    assert not monitor_app.timer.isActive()
