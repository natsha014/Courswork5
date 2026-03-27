import json
from datetime import datetime

import requests
import logging
from celery import shared_task
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from config.settings import TG_API_KEY
from habits.models import Habit

logger = logging.getLogger(__name__)


@shared_task
def create_periodic_tasks():
    PeriodicTask.objects.filter(name__startswith="Send message").delete()
    habits = Habit.objects.all()
    for habit in habits:
        print("Задача добавлена")
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=habit.period,
            period='days',
        )
        text = f"я буду {habit.action} в {habit.time} в {habit.place}"
        PeriodicTask.objects.create(
            interval=schedule,
            name=f"Send message {habit.user.chat_id} {habit.pk}",
            task="habits.tasks.send_message",
            args=json.dumps([text, habit.user.chat_id]),
            start_time=datetime.combine(datetime.now().date(), habit.time),
        )


@shared_task
def send_message(text, chat_id):
    url = f"https://api.telegram.org/bot{TG_API_KEY}/sendMessage"
    params = {"chat_id": chat_id, "text": text}

    try:
        response = requests.get(url, params=params, timeout=5)
        print("Сообщение отправлено")
        response.raise_for_status()
        logger.info(f"Сообщение успешно отправлено в TG для {chat_id}")

    except Exception as e:
        logger.warning("--- ЗАГЛУШКА (TG недоступен) ---")
        logger.warning(f"Кому: {chat_id}")
        logger.warning(f"Текст: {text}")
        logger.warning(f"Причина: {type(e).__name__}")
