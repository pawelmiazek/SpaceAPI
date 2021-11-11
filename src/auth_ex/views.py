from rest_framework import mixins, viewsets, status
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, SetCoreToUserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response


User = get_user_model()


class UserViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = User.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == "reset_password_confirm":
            return SetCoreToUserSerializer

    @action(methods=["get"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.request.user
        return self.retrieve(request, *args, **kwargs)

    @action(
        methods=["patch"],
        detail=True,
    )
    def set_core(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            self.get_object(), data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        core_serializer = UserSerializer(
            self.get_object(), data=request.data, context={"request": request}
        )
        return Response(core_serializer.data, status=status.HTTP_200_OK)
