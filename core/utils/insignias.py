# core/utils/insignias.py
from core.models import Insignia, UsuarioInsignia

def verificar_insignias(usuario):
    insignias = Insignia.objects.all()

    for insignia in insignias:
        if usuario.puntos >= insignia.puntos_necesarios:
            UsuarioInsignia.objects.get_or_create(usuario=usuario, insignia=insignia)
