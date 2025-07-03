from rest_framework import serializers
from core.models import Insignia

class InsigniaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insignia
        fields = '__all__'
