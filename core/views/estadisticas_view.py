from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import Usuario, Proyecto, Actividad, Noticia

class EstadisticasView(APIView):
    def get(self, request):
        data = {
            "usuarios": Usuario.objects.count(),
            "proyectos": Proyecto.objects.count(),
            "actividades": Actividad.objects.count(),
            "noticias": Noticia.objects.count(),
        }
        return Response(data)
