from rest_framework import serializers
from core.models import Barrio

class BarrioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barrio
        fields = '__all__'
