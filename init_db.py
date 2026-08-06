import sqlite3
from werkzeug.security import generate_password_hash

def init_db():
    print("Conectando a la base de datos...")
    conn = sqlite3.connect('papeleria.db')

    print("Leemos el archivo schema.sql")
    with open('schema.sql', 'r', encoding='utf-8') as f:
        schema = f.read()

    print("Ejecutando la creación de tablas")
    conn.executescript(schema)

    # Usuario ADMIN
    print("Creando usuario administrador inicial...")

    # Creacion de la contraseña por defecto
    admin_hash = generate_password_hash("admin123")
    
    # Insert query
    conn.execute(
        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)", ("admin", admin_hash, "admin")
        )

    conn.commit()
    conn.close()
    print("La base de datos y tablas han sido creadas correctamente en papeleria.db")

if __name__ == '__main__':
    init_db()
