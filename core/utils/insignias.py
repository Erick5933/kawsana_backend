from core.models import UsuarioInsignia, Insignia

def verificar_insignias(usuario):
    insignias_ganadas_ids = set(
        UsuarioInsignia.objects.filter(usuario=usuario).values_list("insignia_id", flat=True)
    )
    insignias_disponibles = Insignia.objects.all()

    for insignia in insignias_disponibles:
        if usuario.puntos >= insignia.puntos_necesarios and insignia.id not in insignias_ganadas_ids:
            UsuarioInsignia.objects.create(usuario=usuario, insignia=insignia)
