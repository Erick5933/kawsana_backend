from rest_framework import serializers
from core.models import Parroquia

class ParroquiaSerializer(serializers.ModelSerializer):
    nombre_ciudad = serializers.CharField(source='ciudad.nombre', read_only=True)

    class Meta:
        model = Parroquia
        fields = ['id', 'nombre', 'ciudad', 'nombre_ciudad']
