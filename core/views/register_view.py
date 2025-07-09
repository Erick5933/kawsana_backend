from rest_framework import generics
from rest_framework.permissions import AllowAny
from core.serializers import user_register_serializer

class RegisterView(generics.CreateAPIView):
    serializer_class = user_register_serializer
    permission_classes = [AllowAny]
