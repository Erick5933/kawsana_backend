# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views.LoginUsuarioView import LoginUsuarioView
from core.views import evidencia_view, usuario_view, insignia_view, usuario_insignia_view, EvidenciaActividadViewSet
# Importaciones de views
from core.views.organizacion_view import OrganizacionViewSet
from core.views.proyecto_view import ProyectoViewSet
from core.views.actividad_view import ActividadViewSet
from core.views.progreso_barrio_view import ProgresoBarrioViewSet
from core.views.lider_proyecto_barrio_view import LiderProyectoBarrioViewSet  # CORREGIDO
from core.views.barrio_view import BarrioViewSet
from core.views.noticia_view import NoticiaViewSet
from core.views.reconocimiento_view import ReconocimientoResiduoViewSet
from core.views.usuario_proyecto_view import UsuarioProyectosPorBarrioViewSet
from django.conf import settings
from django.conf.urls.static import static
from core.views.insignias_por_usuario_view import InsigniasPorUsuarioView

from core.views.parroquia_view import ParroquiaViewSet

from core.views.estadisticas_view import EstadisticasView

# Ruteo automático con ViewSets
router = DefaultRouter()
router.register(r'parroquia', ParroquiaViewSet)
router.register(r'evidencias', EvidenciaActividadViewSet)
router.register(r'usuarios', usuario_view.UsuarioViewSet)
router.register(r'insignias', insignia_view.InsigniaViewSet)
router.register(r'usuario-insignias', usuario_insignia_view.UsuarioInsigniaViewSet)
router.register(r'organizaciones', OrganizacionViewSet)
router.register(r'proyectos', ProyectoViewSet)
router.register(r'actividades', ActividadViewSet)
router.register(r'progresos', ProgresoBarrioViewSet)
router.register(r'lideres-proyecto-barrio', LiderProyectoBarrioViewSet)  # CORREGIDO
usuario_proyectos_barrio = UsuarioProyectosPorBarrioViewSet.as_view({
    'get': 'proyectos_barrio',
})
router.register(r'barrios', BarrioViewSet)
router.register(r'noticias', NoticiaViewSet)
router.register(r'reconocimientos', ReconocimientoResiduoViewSet)


# URLs finales
urlpatterns = [
    path('', include(router.urls)),
    path('estadisticas/', EstadisticasView.as_view(), name='estadisticas'),
    path('login/', LoginUsuarioView.as_view(), name='login_usuario'),
    path('usuarios/<int:pk>/proyectos-barrio/', usuario_proyectos_barrio, name='usuario-proyectos-barrio'),
    path('usuarios/<int:usuario_id>/insignias-desbloqueadas/', InsigniasPorUsuarioView.as_view(), name='insignias-por-usuario'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)