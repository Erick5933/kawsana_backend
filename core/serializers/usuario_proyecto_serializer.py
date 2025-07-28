from rest_framework import serializers
from core.models import UsuarioProyecto

class UsuarioProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioProyecto
        fields = '__all__'
