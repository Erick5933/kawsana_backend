from rest_framework import serializers
from core.models import LiderProyectoBarrio

class LiderProyectoBarrioSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiderProyectoBarrio
        fields = ['id', 'usuario', 'proyecto', 'barrio']
