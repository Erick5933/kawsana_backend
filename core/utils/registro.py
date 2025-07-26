from core.models import LiderProyectoBarrio, UsuarioProyecto

def inscribir_lider_y_usuarios(lider_usuario, proyecto):
    barrio = lider_usuario.barrio
    if not barrio:
        raise Exception("El líder no tiene barrio asignado")

    # Registrar al líder
    lider_proyecto_barrio, _ = LiderProyectoBarrio.objects.get_or_create(
        usuario=lider_usuario,
        proyecto=proyecto,
        barrio=barrio,
    )

    # Inscribir automáticamente a todos los usuarios del barrio
    usuarios = barrio.usuarios.filter(estado=True)
    for usuario in usuarios:
        UsuarioProyecto.objects.get_or_create(usuario=usuario, proyecto=proyecto)
