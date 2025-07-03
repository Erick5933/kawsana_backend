from rest_framework import serializers
from core.models import ProgresoBarrio

class ProgresoBarrioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgresoBarrio
        fields = '__all__'
