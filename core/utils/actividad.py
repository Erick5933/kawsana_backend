from core.models import Usuario, UsuarioInsignia
from core.utils.insignias import verificar_insignias


def completar_actividad(actividad):
    barrio = actividad.proyecto.barrio_set.first()
    if not barrio:
        return

    usuarios = Usuario.objects.filter(barrio=barrio)
    for usuario in usuarios:
        usuario.puntos += actividad.puntos
        usuario.save()
        verificar_insignias(usuario)
