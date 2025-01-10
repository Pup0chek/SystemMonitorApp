import os
import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import Database

@pytest.fixture
def db():
    db_instance = Database()
    db_instance.connect_to_db()
    yield db_instance
    db_instance.close()
    if os.path.exists("system_monitor.db"):
        os.remove("system_monitor.db")

def test_connect_to_db(db):
    assert db.connection is not None

def test_create_table(db):
    cursor = db.connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='monitor_data';")
    result = cursor.fetchone()
    assert result is not None

def test_insert_and_fetch_data(db):
    db.save_to_db(50, 4.0, 8.0, 200.0, 100.0)
    records = db.fetch_all_records()
    assert len(records) == 1
    assert records[0][2] == 50
