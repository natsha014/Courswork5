from rest_framework import serializers

from habits.models import Habit
from habits.validators import RewardValidator, TimeToActionValidator, ConnectionHabitValidator, \
    PleasantHabitValidator, PeriodValidator


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            RewardValidator(field1='reward', field2='connection_habit'),
            TimeToActionValidator(field='time_to_action'),
            ConnectionHabitValidator(field='connection_habit'),
            PleasantHabitValidator(),
            PeriodValidator(),
        ]


class HabitPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ('action', 'place', 'time', 'period', 'is_pleasant')
