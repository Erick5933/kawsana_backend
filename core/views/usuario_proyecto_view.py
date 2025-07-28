# core/views/usuario_proyecto_view.py
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from core.models import Usuario, LiderProyectoBarrio
from core.serializers.proyecto_serializer import ProyectoSerializer  # asegúrate de tenerlo

class UsuarioProyectosPorBarrioViewSet(viewsets.ViewSet):

    @action(detail=True, methods=['get'], url_path='proyectos-barrio')
    def proyectos_barrio(self, request, pk=None):
        try:
            usuario = Usuario.objects.get(pk=pk)
            barrio = usuario.barrio
            if not barrio:
                return Response({"error": "El usuario no tiene barrio asignado."}, status=400)

            # Obtener todos los proyectos donde el barrio está inscrito
            liderazgos = LiderProyectoBarrio.objects.filter(barrio=barrio)
            proyectos = [liderazgo.proyecto for liderazgo in liderazgos]
            serializer = ProyectoSerializer(proyectos, many=True)
            return Response(serializer.data)

        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=404)
