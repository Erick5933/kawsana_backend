from rest_framework import viewsets
from core.models import ProgresoBarrio
from core.serializers.progreso_barrio_serializer import ProgresoBarrioSerializer

from rest_framework.decorators import action
from rest_framework.response import Response

class ProgresoBarrioViewSet(viewsets.ModelViewSet):
    queryset = ProgresoBarrio.objects.all()
    serializer_class = ProgresoBarrioSerializer

    @action(detail=False, methods=['get'], url_path='por-barrio-proyecto')
    def get_by_barrio_proyecto(self, request):
        barrio_id = request.query_params.get("barrio_id")
        proyecto_id = request.query_params.get("proyecto_id")

        if not barrio_id or not proyecto_id:
            return Response({"error": "Faltan parámetros"}, status=400)

        try:
            progreso = ProgresoBarrio.objects.get(barrio_id=barrio_id, proyecto_id=proyecto_id)
            serializer = self.get_serializer(progreso)
            return Response(serializer.data)
        except ProgresoBarrio.DoesNotExist:
            return Response({"error": "Progreso no encontrado"}, status=404)
