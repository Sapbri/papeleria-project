import sqlite3
from flask import g

DATABASE = 'papeleria.db'

def get_db():
    """Abre una nueva conexión si no existe una para la petición actual."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            DATABASE,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Permite acceder a las columnas por nombre como si fuera un diccionario:
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """Cierra la conexión a la base de datos al terminar la petición."""
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
    """Registra la función de cierre en la aplicación de Flask."""
    app.teardown_appcontext(close_db)