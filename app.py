import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "clave_secreta"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///datos.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "uploads")
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

from models import db

db.init_app(app)


from gestor import GestorBaseDatos

AREAS = {
    "EF": "Ecofisiología",
    "ES": "Ecosistema",
    "AE": "Agroecología",
    "RN": "Recursos Naturales",
    "CA": "Comunicación ambiental",
}


@app.route("/")
def inicio():
    respInicio = redirect(url_for("enviarTrabajo"))
    return respInicio


@app.route("/enviar-trabajo", methods=["GET", "POST"])
def enviarTrabajo():
    respuesta = None

    if request.method == "POST":
        titulo = request.form.get("titulo")
        resumen = request.form.get("resumen")
        area = request.form.get("area")
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        correo = request.form.get("correo")
        archivo = request.files.get("archivo")
        nomArchivo = None

        if archivo and archivo.filename != "":
            nomArchivo = secure_filename(archivo.filename)
            archivo.save(os.path.join(app.config["UPLOAD_FOLDER"]), nomArchivo)

        try:
            trabajoGuardado = GestorBaseDatos.registrarTrabajo(
                titulo=titulo,
                resumen=resumen,
                area=area,
                nombre=nombre,
                apellido=apellido,
                correo=correo,
                archivo_nombre=nomArchivo,
            )

            flash(
                f"TRABAJO CARGADO CORRECTAMENTE! Número de consulta: {trabajoGuardado}"
            )
        except Exception as e:
            db.session.rollback()
            flash(
                "Ocurrió un error al cargar el trabajo. Por favor, intente nuevamente."
            )
            print(f"ERROR: {e}")

        respuesta = redirect(url_for("enviarTrabajo"))

    else:
        respuesta = render_template("enviar_trabajo.html", area=AREAS)

    return respuesta


@app.route("/organizador/panel", methods=["GET"])
def panelOrganizador():
    respuestaPanel = render_template("panel_organizador.html")
    return respuestaPanel


@app.route("/organizador/asignar", methods=["POST"])
def asignarAutomatico():
    respuesta = None

    try:
        cantidad = GestorBaseDatos.asignarEvaluadoresAutomatico()

        if cantidad > 0:
            flash(
                f"PROCESO COMPLETADO! Se asignaron evaluadores a {cantidad} trabajos.",
                "success",
            )
        else:
            flash(
                "No había trabajos pendientes que cumplieran con los requisitos para ser asignados",
                "info",
            )
    except Exception as e:
        db.session.rollback()
        flash("Ocurrio un error en el servidor durante la asignación.", "error")
        print(f"ERROR: {e}")

    respuesta = redirect(url_for("enviarTrabajo"))
    return respuesta


if __name__ == "__main__":
    app.run(debug=True)
