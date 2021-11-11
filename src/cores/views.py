from rest_framework import mixins, viewsets
from .models import Core
from .serializers import CoreSerializer
from rest_framework.permissions import IsAuthenticated


class CoreViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Core.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = CoreSerializer

    def get_queryset(self):
        if not self.queryset:
            "fetch_cores"
            return Core.objects.all()
        return self.queryset
