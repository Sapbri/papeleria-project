import sqlite3

def init_db():
    print("Conectando a la base de datos...")
    conn = sqlite3.connect('papeleria.db')

    print("Leemos el archivo schema.sql")
    with open('schema.sql', 'r', encoding='utf-8') as f:
        schema = f.read()

    print("Ejecutando la creación de tablas")
    conn.executescript(schema)

    conn.commit()
    conn.close()
    print("La base de datos y tablas han sido creadas correctamente en papeleria.db")

if __name__ == '__main__':
    init_db()
