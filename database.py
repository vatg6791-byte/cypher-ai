import sqlite3
from datetime import datetime

class CypherSecurityCore:
    def __init__(self, db_name="cypher_vault.db"):
        self.db_name = db_name
        self._initialize_vault()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def _initialize_vault(self):
        with self._get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS operational_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    node_role TEXT NOT NULL,
                    payload_data TEXT NOT NULL,
                    execution_timestamp TEXT NOT NULL
                )
            ''')
            conn.commit()

    def record_payload(self, role, data):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO operational_logs (node_role, payload_data, execution_timestamp) VALUES (?, ?, ?)",
                (role, data, timestamp)
            )
            conn.commit()

    def extract_all_logs(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT node_role, payload_data, execution_timestamp FROM operational_logs ORDER BY id ASC")
            return [dict(row) for row in cursor.fetchall()]

if __name__ == "__main__":
    vault = CypherSecurityCore()
    print("[+] Cypher SQLite Vault initialized successfully and secured.")
