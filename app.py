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

@app.after_request
def after_request(response):
    """Asegura que las respuestas no son guardadas en el navegador"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET"])
@login_required
def index():
    return render_template("index.html")


@app.route("/cambiar_clave", methods=["GET", "POST"])
@login_required
def change_password():
    '''Cambiar la contraseña del usuario'''

    # Revisar si la peticion es POST o GET
    if request.method == "POST":

        # Extraer la informacion del form
        current_password = request.form.get("current_password").strip()
        new_password = request.form.get("new_password").strip()
        confirmation_password = request.form.get("confirmation_password").strip()

        # Comprobar que no hay espacios adicionales o que los campos estan en blanco
        if not current_password:
            return apology("Debe digitar su contraseña actual", 400)

        if not new_password:
            return apology("Debe digitar su nueva contraseña", 400)

        if not confirmation_password:
            return apology("Debe digitar su nueva contraseña para confirmarla", 400)

        # Comprobar que la contraseña escrita es la misma que la contraseña confirmada.
        if new_password != confirmation_password:
            return apology("Su nueva contraseña NO es igual. Comprueba que la contraseña digitada en el campo de confimracion sea la misma que la del campo de nueva contraseña.", 403)

        # Comprobar que la contraseña escrita es diferente a la contraseña anterior.
        if current_password == new_password:
            return apology("Su nueva contraseña no puede ser la misma que su contraseña anterior. Digite una contraseña diferente a la anterior", 400)

        # Query database para el hash del usuario que cambia la contraseña
        conexion = db.get_db()
        user_hash_password = conexion.execute(
            "SELECT password_hash FROM users WHERE id = ?", (session["user_id"],)
        ).fetchone()

        # Comprobar la contraseña actual sea la misma que digito
        if not check_password_hash(user_hash_password["password_hash"], current_password):
            return apology("Contraseña actual inválida. Su contraseña actual es diferente a la digitada en el campo de contraseña actual. Verifique.", 400)

        # Hash la nueva clave del usuario
        hash_new_user_password = generate_password_hash(new_password)

        # Update la nueva clave del usuario
        conexion.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?", (hash_new_user_password, session["user_id"])
        )

        # Guardar cambios en la BD
        conexion.commit()

        # Redirigir el usuario a la pagina home o index
        return redirect("/")

    else:
        return render_template("change_password.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Inicia Sesion del usuario"""

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

        # Recordar que usuario es el que esta en la sesión y su rol.
        session["user_id"] = resultado_username_login[0]["id"]
        session["username"] = resultado_username_login[0]["username"]
        session["user_role"] = resultado_username_login[0]["role"]

        # Redirigir el usuario a la pagina home o index
        return redirect("/")

    # El usuario llega por la ruta GET (luego de hacer click en el link o redireccionado)
    else:
        return render_template("login.html")