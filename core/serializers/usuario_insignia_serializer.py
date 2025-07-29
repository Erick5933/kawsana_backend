# core/serializers/usuario_insignia_serializer.py
from rest_framework import serializers
from core.models import UsuarioInsignia
from core.serializers.insignia_serializer import InsigniaSerializer

class UsuarioInsigniaSerializer(serializers.ModelSerializer):
    insignia = InsigniaSerializer(read_only=True)

    class Meta:
        model = UsuarioInsignia
        fields = '__all__'
