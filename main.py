import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

class DatabaseManager:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def create_table(self, table_name, columns):
        columns_definition = ', '.join([f"{col} {datatype}" for col, datatype in columns.items()])
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition})")
        self.connection.commit()

    def insert_data(self, table_name, data):
        placeholders = ', '.join(['?' for _ in data])
        self.cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", data)
        self.connection.commit()

    def fetch_data(self, table_name, condition=None):
        query = f"SELECT * FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        return self.cursor.execute(query).fetchall()

    def update_data(self, table_name, set_values, condition):
        set_clause = ', '.join([f"{col} = '{value}'" for col, value in set_values.items()])
        self.cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {condition}")
        self.connection.commit()

    def delete_data(self, table_name, condition):
        self.cursor.execute(f"DELETE FROM {table_name} WHERE {condition}")
        self.connection.commit()

    def export_to_csv(self, table_name, file_name):
        df = pd.read_sql(f"SELECT * FROM {table_name}", self.connection)
        df.to_csv(file_name, index=False)

    def visualize_data(self, data):
        df = pd.DataFrame(data)
        df.plot(kind='bar')
        plt.show()

    def close(self):
        self.connection.close()

# Пример использования
db_manager = DatabaseManager('my_database.db')
db_manager.create_table('users', {'id': 'INTEGER PRIMARY KEY', 'name': 'TEXT', 'age': 'INTEGER'})

data = db_manager.fetch_data('users')
db_manager.visualize_data(data)
db_manager.export_to_csv('users', 'users_data.csv')
db_manager.close()
