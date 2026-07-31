import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

import db
from helpers import apology, login_required

# Configurar app
app = Flask(__name__)

# Configurar Flask-Session para guardar las sesiones en el servidor (archivos locales)
    # La sesion expira apenas se cierre el navegador
app.config["SESSION_PERMANENT"] = False
    # Flask guarda los datos reales de la sesión en una carpeta en el servidor/disco duro, en lugar de meter esos datos en las cookies del usuario
app.config["SESSION_TYPE"] = "filesystem"
    # Activa oficialmente la libreria dentro de app
Session(app)

# Le decimos a Flask que use las reglas de cierre de db.py:
db.init_app(app)

@app.route("/", methods=["GET"])
@login_required
def index():
    # Probamos la conexión haciendo un conteo de productos
    conexion = db.get_db()
    resultado = conexion.execute('SELECT COUNT(*) AS total FROM products').fetchone()
    total = resultado['total'] 

    return f"<h1>¡Conexión Exitosa!</h1><p>Productos en el sistema: {total}</p>"


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Borra cualquier user_id
    session.clear()

    # El usuario llega por la ruta POST (luego de enviar el formulario POST)
    if request.method == "POST":
        # Nos aseguramos que username fue enviado
        if not request.form.get("username"):
            return apology("Debe enviar un username", 400)

        # No aseguramos que password fue enviado.
        if not request.form.get("password"):
            return apology("Debe enviar una contraseña", 400)

        # Query database para username
        conexion = db.get_db()
        resultado_username_login = conexion.execute(
            "SELECT * FROM users WHERE username = ?", (request.form.get("username"),)
        ).fetchall()

        # Nos aseguramos que username exista y que la contraseña sea correcta
        if len(resultado_username_login) != 1 or not check_password_hash(
            resultado_username_login[0]["password_hash"], request.form.get("password")
        ):
            return apology("El username y/o contraseña es inválido", 400)

        # Recordar que usuario es el que esta en la sesión
        session["user_id"] = resultado_username_login[0]["id"]

        # Redirigir el usuario a la pagina home o index
        return redirect("/")

    # El usuario llega por la ruta GET (luego de hacer click en el link o redireccionado)
    else:
        return render_template("login.html")