from flask import redirect, session, render_template
# Crear decorators sin que se afecte la funcion original
from functools import wraps


def apology(message, code=400):
    """Muestra una página de error."""
    return render_template("apology.html", top=code, message=message), code


def login_required(f):
    """
    Decorate rutas que requieren iniciar sesion.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function