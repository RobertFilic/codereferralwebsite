import sqlite3
import time
from datetime import datetime, timedelta

class DatabaseManager:
    def __init__(self, db_file='referral_codes.db'):
        self.db_file = db_file
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS services (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS codes (id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT UNIQUE NOT NULL, service_id INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, valid_until TIMESTAMP NOT NULL, description TEXT, is_valid BOOLEAN NOT NULL DEFAULT 1, FOREIGN KEY (service_id) REFERENCES services (id))''')
        conn.commit()
        conn.close()

    def execute_query(self, query, params=(), retries=3, retry_delay=0.1):
        retries_remaining = retries
        while retries_remaining > 0:
            try:
                conn = sqlite3.connect(self.db_file)
                c = conn.cursor()
                c.execute(query, params)
                result = c.fetchall()
                conn.commit()
                return result
            except sqlite3.OperationalError as e:
                if 'database is locked' in str(e):
                    retries_remaining -= 1
                    if retries_remaining > 0:
                        time.sleep(retry_delay)
                    else:
                        raise e
                else:
                    raise e
            finally:
                conn.close()

    def commit(self):
        conn = sqlite3.connect(self.db_file)
        conn.commit()
        conn.close()

    def close(self):
        pass  # Connection is closed after each query, so no need for an explicit close method