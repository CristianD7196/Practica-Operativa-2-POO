from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Organizador(db.Model):
    __tablename__ = "organizadores"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    clave = db.Column(db.String(100), nullable=False, default="admin")


class Evaluador(db.Model):
    __tablename__ = "evaluadores"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(5))
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    area = db.Column(db.String(3), nullable=False)
    max_trabajos = db.Column(db.Integer, nullable=False, default=3)
    clave = db.Column(db.String(100), nullable=False, default="123")
    asignaciones = db.relationship("Asignacion", backref="evaluador", lazy=True)


class Trabajo(db.Model):
    __tablename__ = "trabajos"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    resumen = db.Column(db.Text, nullable=False)
    area = db.Column(db.String(3), nullable=False)
    autor_nombre = db.Column(db.String(100), nullable=False)
    autor_apellido = db.Column(db.String(100), nullable=False)
    autor_email = db.Column(db.String(120), nullable=False)
    estado = db.Column(db.String(20), default="Pendiente")
    fecha_envio = db.Column(db.DateTime, default=datetime.now)
    archivo_nombre = db.Column(db.String(255), nullable=True)
    asignaciones = db.relationship("Asignacion", backref="trabajo", lazy=True)


class Asignacion(db.Model):
    __tablename__ = "asignaciones"
    id = db.Column(db.Integer, primary_key=True)
    trabajo_id = db.Column(db.Integer, db.ForeignKey("trabajos.id"), nullable=False)
    evaluador_id = db.Column(
        db.Integer, db.ForeignKey("evaluadores.id"), nullable=False
    )
    valoracion = db.Column(db.Integer, nullable=True)
    comentarios = db.Column(db.Text, nullable=True)
    fecha_evaluacion = db.Column(db.DateTime, nullable=True)
