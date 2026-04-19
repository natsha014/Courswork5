from datetime import timedelta

from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, verbose_name="Создатель")
    place = models.CharField(max_length=100, verbose_name="Место")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=100, verbose_name="Действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Признак приятной привычки")
    connection_habit = models.ForeignKey('self', on_delete=models.SET_NULL, **NULLABLE,
                                         verbose_name="Связанная привычка", related_name="related_habits")
    period = models.PositiveIntegerField(default=1, verbose_name="Периодичность")
    reward = models.CharField(max_length=100, **NULLABLE, verbose_name="Вознаграждение")
    time_to_action = models.DurationField(default=timedelta(seconds=60), verbose_name="Время на выполнения")
    is_published = models.BooleanField(default=True, verbose_name="Признак публичности")

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'

    def __str__(self):
        return f"я буду {self.action} в {self.time} в {self.place}"
