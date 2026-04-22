import sqlite3
from e_service import hash_password

conn = sqlite3.connect('database.db')

conn.execute('''
    INSERT INTO users (full_name, email, password, role)
    VALUES (?, ?, ?, ?)
''', ('Admin', 'admin@esui.edu.ng', hash_password('admin123'), 'admin'))

conn.commit()
conn.close()
print("Admin created.")