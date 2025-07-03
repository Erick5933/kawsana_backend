from rest_framework import serializers
from core.models import LiderProyecto

class LiderProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiderProyecto
        fields = '__all__'
