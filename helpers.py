from flask import redirect, session, render_template
# Crear decorators sin que se afecte la funcion original
from functools import wraps


def apology(message, code=400):
    '''Muestra una página de error.'''

    return render_template("apology.html", top=code, message=message), code


def login_required(f):
    '''Decorador para las rutas que requieren iniciar sesion.'''

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    '''Verifica que la persona tenga sesion con rol de admin'''

    @wraps(f)
    def decorated_function(*args, **kwargs):

        # Comprobar que este logueado por si acaso no se usó @login_required
        if session.get("user_id") is None:
            return redirect("/login")

        # Comprobar que el usuario tiene rol admin
        if session.get("user_role") != "admin":
            return apology("Acceso denegado: Se requieren permisos de administrador", 403)
        
        return f(*args, **kwargs)

    return decorated_function