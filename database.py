import sqlite3
class Database:
    def __init__(self):
        self.connection = None

    def connect_to_db(self):
        try:
            self.connection = sqlite3.connect("system_monitor.db")
            cursor = self.connection.cursor()
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
            self.connection.commit()
        except Exception as e:
            raise RuntimeError(f"Ошибка подключения к базе данных: {e}")

    def save_to_db(self, cpu, ram_available, ram_total, disk_free, disk_total):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO monitor_data (cpu_usage, ram_available, ram_total, disk_free, disk_total) VALUES (?, ?, ?, ?, ?)",
                (cpu, ram_available, ram_total, disk_free, disk_total)
            )
            self.connection.commit()
        except Exception as e:
            raise RuntimeError(f"Ошибка записи данных в базу данных: {e}")

    def fetch_all_records(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM monitor_data")
            return cursor.fetchall()
        except Exception as e:
            raise RuntimeError(f"Ошибка при чтении данных из базы данных: {e}")

    def close(self):
        if self.connection:
            self.connection.close()
