from app import app
from models import db, Evaluador

with app.app_context():
    ev1 = Evaluador(nombre="Carlos", apellido="Sánchez", area="EF", max_trabajos=5)
    ev2 = Evaluador(nombre="María", apellido="Pérez", area="EF", max_trabajos=3)
    ev3 = Evaluador(nombre="Juan", apellido="Gómez", area="EF", max_trabajos=4)

    db.session.add_all([ev1, ev2, ev3])
    db.session.commit()
    print("¡Evaluadores cargados con éxito!")
