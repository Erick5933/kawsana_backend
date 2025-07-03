from rest_framework import serializers
from core.models import Organizacion

class OrganizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizacion
        fields = '__all__'
