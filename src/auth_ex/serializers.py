from rest_framework import serializers
from django.contrib.auth import get_user_model

from cores.models import Core
from cores.serializers import CoreSerializer


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    core_id = serializers.PrimaryKeyRelatedField(
        source="core", queryset=Core.objects.all(), write_only=True
    )
    core = CoreSerializer(read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "core_id", "core")
