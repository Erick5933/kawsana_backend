from rest_framework import serializers
from core.models import EvidenciaActividad

class EvidenciaActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvidenciaActividad
        fields = '__all__'
