import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name # Сохраняем имя базы данных
        self.conn = None # Инициализируем как None

    def get_connection(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_name)

        return self.conn

    def create_table(self, column_names):
        conn = self.get_connection()
        with conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS mydata")
            columns_str = ", ".join([f"C{col} TEXT" for col in column_names])
            create_query = f"""
                CREATE TABLE IF NOT EXISTS mydata (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {columns_str}
                )
            """
            cursor.execute(create_query)

    def close(self):
        self.conn = None

