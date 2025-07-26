from rest_framework import serializers
from core.models import Usuario, Barrio

class UsuarioSerializer(serializers.ModelSerializer):
    barrio = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Usuario
        fields = '__all__'


class BarrioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barrio
        fields = ['id', 'nombre']