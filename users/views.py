from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from habits.permissions import IsOwner
from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        return UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [IsOwner()]

        return super().get_permissions()
