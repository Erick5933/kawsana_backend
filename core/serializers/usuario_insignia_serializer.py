from rest_framework import serializers
from core.models import UsuarioInsignia

class UsuarioInsigniaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioInsignia
        fields = '__all__'
