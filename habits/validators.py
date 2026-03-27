from datetime import timedelta

from rest_framework.exceptions import ValidationError


class RewardValidator:
    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, value):
        reward = value.get(self.field1)
        connection_habit = value.get(self.field2)

        if connection_habit and reward:
            raise ValidationError(
                "Нельзя одновременно выбирать вознаграждение и связанную привычку."
            )


class TimeToActionValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        time_to_action = value.get(self.field)

        if time_to_action and time_to_action > timedelta(minutes=2):
            raise ValidationError("Время выполнения не может больше 120 секунд")


class ConnectionHabitValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        connection_habit = value.get(self.field)

        if connection_habit and not connection_habit.is_pleasant:
            raise ValidationError("Связанные привычки могут быть только с признаком приятной привычки.")


class PleasantHabitValidator:
    def __call__(self, value):
        if value.get('is_pleasant') and (value.get('reward') or value.get('connection_habit')):
            raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки.")


class PeriodValidator:
    def __call__(self, value):
        period = value.get('period')
        if period and period > 7:
            raise ValidationError("Нельзя выполнять привычку больше 7 раз в неделю.")
        if period and period < 1:
            raise ValidationError("Период не может быть меньше 1 дня.")
