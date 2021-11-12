from rest_framework import mixins, viewsets
from .models import Core
from .serializers import CoreSerializer
from rest_framework.permissions import IsAuthenticated
from .services import fetch_cores_service


class CoreViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Core.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = CoreSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if not queryset:
            fetch_cores_service.fetch_data(0, False, False, all_cores_to_db=True)
            return Core.objects.all()
        return queryset
