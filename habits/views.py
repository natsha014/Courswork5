from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

from habits.models import Habit
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer, HabitPublicSerializer
from habits.paginators import HabitPaginator


class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'public':
            return HabitPublicSerializer
        return HabitSerializer

    def get_queryset(self):
        if self.action == 'public':
            return Habit.objects.filter(is_published=True)
        return Habit.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.action == 'public':
            return [AllowAny()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def public(self, request):
        return super().list(request)
