from rest_framework import serializers
from core.models import ReconocimientoResiduo

class ReconocimientoResiduoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReconocimientoResiduo
        fields = '__all__'
