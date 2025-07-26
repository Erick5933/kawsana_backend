from core.models import Usuario, LiderProyectoBarrio
from core.utils.insignias import verificar_insignias

def completar_actividad(actividad, usuario_lider):
    try:
        # Obtener la relación líder-proyecto-barrio
        lider_barrio = LiderProyectoBarrio.objects.get(
            usuario=usuario_lider,
            proyecto=actividad.proyecto
        )
        barrio = lider_barrio.barrio
    except LiderProyectoBarrio.DoesNotExist:
        return

    # Obtener todos los usuarios del mismo barrio
    usuarios_barrio = Usuario.objects.filter(barrio=barrio)

    for usuario in usuarios_barrio:
        usuario.puntos += actividad.puntos
        usuario.save()
        verificar_insignias(usuario)
