from models import db, Trabajo, Evaluador, Asignacion
from datetime import datetime


class GestorBaseDatos:

    @classmethod
    def registrarTrabajo(
        cls, titulo, resumen, area, nombre, apellido, correo, nomArchivo
    ):
        nuevoTrabajo = Trabajo(
            titulo=titulo,
            resumen=resumen,
            area=area,
            autor_nombre=nombre,
            autor_apellido=apellido,
            autor_email=correo,
            estado="Pendiente",
            fecha_envio=datetime.now(),
            archivo_nombre=nomArchivo,
        )

        db.session.add(nuevoTrabajo)
        db.session.commit()

        return nuevoTrabajo

    @classmethod
    def asignarEvaluadoresAutomatico(cls):
        trabajosPendientes = Trabajo.query.filter_by(estado="Pendiente").all()
        trabajosProcesados = 0

        for trabajo in trabajosPendientes:
            asignacionesActuales = len(trabajo.asignaciones)
            faltan = 3 - asignacionesActuales

            if faltan > 0:
                evaluadores = Evaluador.query.all()

                evaluadoresCandidatos = []

                for ev in evaluadores:
                    if (
                        ev.area == trabajo.area
                        and len(ev.asignaciones) < ev.max_trabajos
                    ):
                        evaluadoresCandidatos.append(ev)

                nuevosAsignados = []

                for evaluador in evaluadoresCandidatos:
                    estaAsignado = False

                    for asig in trabajo.asignaciones:
                        if asig.evaluador_id == evaluador.id:
                            estaAsignado = True

                    if not estaAsignado and len(nuevosAsignados) < faltan:
                        nuevosAsignados.append(evaluador)

                if len(nuevosAsignados) == faltan:
                    for ev in nuevosAsignados:
                        nuevaAsig = Asignacion(
                            trabajo_id=trabajo.id, evaluador_id=ev.id
                        )
                        db.session.add(nuevaAsig)

                    trabajo.estado = "Asignado"
                    trabajosProcesados = trabajosProcesados + 1
        db.session.commit()
        return trabajosProcesados

    @classmethod
    def registrarEvaluador(cls, nombre, apellido, area, max_trabajos):
        nuevoEvaluador = Evaluador(
            nombre=nombre, apellido=apellido, area=area, max_trabajos=max_trabajos
        )

        db.session.add(nuevoEvaluador)
        db.session.commit()
