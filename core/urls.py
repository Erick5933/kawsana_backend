# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Importaciones de views
from core.views.organizacion_view import OrganizacionViewSet
from core.views.proyecto_view import ProyectoViewSet
from core.views.actividad_view import ActividadViewSet
from core.views.evidencia_view import EvidenciaActividadViewSet
from core.views.progreso_barrio_view import ProgresoBarrioViewSet
from core.views.lider_proyecto_barrio_view import LiderProyectoBarrioViewSet  # CORREGIDO
from core.views.barrio_view import BarrioViewSet
from core.views.usuario_view import UsuarioViewSet
from core.views.noticia_view import NoticiaViewSet
from core.views.reconocimiento_view import ReconocimientoResiduoViewSet
from core.views.insignia_view import InsigniaViewSet
from core.views.usuario_insignia_view import UsuarioInsigniaViewSet

# Ruteo automático con ViewSets
router = DefaultRouter()
router.register(r'organizaciones', OrganizacionViewSet)
router.register(r'proyectos', ProyectoViewSet)
router.register(r'actividades', ActividadViewSet)
router.register(r'evidencias', EvidenciaActividadViewSet)
router.register(r'progresos', ProgresoBarrioViewSet)
router.register(r'lideres-proyecto-barrio', LiderProyectoBarrioViewSet)  # CORREGIDO

router.register(r'barrios', BarrioViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'noticias', NoticiaViewSet)
router.register(r'reconocimientos', ReconocimientoResiduoViewSet)
router.register(r'insignias', InsigniaViewSet)
router.register(r'usuarios-insignias', UsuarioInsigniaViewSet)

# URLs finales
urlpatterns = [
    path('', include(router.urls)),
]
