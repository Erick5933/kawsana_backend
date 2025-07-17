from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Usuario
from django.contrib.auth.hashers import check_password  # si usas contraseñas encriptadas
from rest_framework.permissions import AllowAny

class LoginUsuarioView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        usuario = request.data.get('usuario')
        contraseña = request.data.get('contraseña')

        if not usuario or not contraseña:
            return Response({'error': 'Debe proporcionar usuario y contraseña.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Usuario.objects.get(usuario=usuario)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if not user.estado:
            return Response({'error': 'Usuario inactivo.'}, status=status.HTTP_403_FORBIDDEN)

        # Si usas contraseñas en texto plano (no recomendado), haz:
        if user.contraseña != contraseña:
            return Response({'error': 'Contraseña incorrecta.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Si usas contraseñas encriptadas (mejor práctica):
        # if not check_password(contraseña, user.contraseña):
        #     return Response({'error': 'Contraseña incorrecta.'}, status=status.HTTP_401_UNAUTHORIZED)

        mensaje = ""
        if user.tipo_usuario == "ciudadano":
            mensaje = "Bienvenido Ciudadano"
        elif user.tipo_usuario == "lider":
            mensaje = "Bienvenido Líder"
        elif user.tipo_usuario == "organizacion":
            mensaje = "Bienvenido Organización"

        return Response({
            'mensaje': mensaje,
            'tipo_usuario': user.tipo_usuario,
            'id_usuario': user.id,
            'nombres': user.nombres,
            'apellidos': user.apellidos
        }, status=status.HTTP_200_OK)
