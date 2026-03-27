from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from habits.models import Habit
from habits.tasks import create_periodic_tasks


@receiver([post_save, post_delete], sender=Habit)
def update_habit_schedule(sender, instance, **kwargs):
    create_periodic_tasks.delay()
