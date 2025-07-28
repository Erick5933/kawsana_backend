from rest_framework import serializers
from core.models import LiderProyectoBarrio

class LiderProyectoBarrioSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiderProyectoBarrio
        fields = '__all__'
