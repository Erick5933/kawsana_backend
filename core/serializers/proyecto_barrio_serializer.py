from rest_framework import serializers
from core.models import ProyectoBarrio

class ProyectoBarrioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProyectoBarrio
        fields = '__all__'
