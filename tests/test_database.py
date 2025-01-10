import pytest
import sys
import os
import sqlite3

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

@pytest.fixture
def test_db():
    db = Database()
    db.connection = sqlite3.connect(":memory:")
    cursor = db.connection.cursor()
    cursor.execute("""
        CREATE TABLE monitor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            cpu_usage REAL,
            ram_available REAL,
            ram_total REAL,
            disk_free REAL,
            disk_total REAL
        )
    """)
    db.connection.commit()
    return db

def test_save_to_db(test_db):
    test_db.save_to_db(10.5, 4.2, 8.0, 100.5, 200.0)


    cursor = test_db.connection.cursor()
    cursor.execute("SELECT * FROM monitor_data")
    results = cursor.fetchall()

    assert len(results) == 1
    assert results[0][2:] == (10.5, 4.2, 8.0, 100.5, 200.0)

def test_fetch_all_records(test_db):
    cursor = test_db.connection.cursor()
    cursor.execute(
        "INSERT INTO monitor_data (cpu_usage, ram_available, ram_total, disk_free, disk_total) VALUES (?, ?, ?, ?, ?)",
        (15.0, 3.5, 7.0, 120.0, 250.0)
    )
    test_db.connection.commit()


    records = test_db.fetch_all_records()


    assert len(records) == 1
    assert records[0][2:] == (15.0, 3.5, 7.0, 120.0, 250.0)