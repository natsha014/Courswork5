from rest_framework.test import APITestCase
from rest_framework import status
from habits.models import Habit
from users.models import User
from datetime import timedelta, time


class HabitTestCase(APITestCase):

    def setUp(self):
        # 1. Создаем пользователя
        self.user = User.objects.create(email="test@test.ru")
        self.user.set_password("12345")
        self.user.save()
        # 2. Авторизуем его (тесты будут идти от его имени)
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        """Тест создания полезной привычки"""
        data = {
            "place": "Дом",
            "time": time(10, 0, 0),
            "action": "Зарядка",
            "is_pleasant": False,
            "period": 1,
            "reward": "Кофе",
            "time_to_action": timedelta(minutes=1)
        }
        response = self.client.post('/habits/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.get().action, "Зарядка")

    def test_time_validator(self):
        """Тест: время выполнения не более 120 секунд"""
        data = {
            "place": "Дом",
            "time": time(10, 0, 0),
            "action": "Долгое действие",
            "time_to_action": timedelta(minutes=5)  # больше 120 c
        }
        response = self.client.post('/habits/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pleasant_habit_no_reward(self):
        """Тест: у приятной привычки не может быть вознаграждения"""
        data = {
            "place": "Дом",
            "time": time(10, 0, 0),
            "action": "Фильм",
            "is_pleasant": True,
            "reward": "Шоколадка"  # ОШИБКА по ТЗ
        }
        response = self.client.post('/habits/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_habit(self):
        """Тест: пользователь видит только свои привычки"""
        # Создаем привычку для текущего юзера
        Habit.objects.create(user=self.user, action="Моя", place="X", time=time(12, 0),
                             time_to_action=timedelta(minutes=1))

        # Создаем другого юзера и его привычку
        other_user = User.objects.create(email="other@test.ru")
        other_user.set_password("password")
        other_user.save()
        Habit.objects.create(user=other_user, action="Чужая", place="Y", time=time(12, 0),
                             time_to_action=timedelta(minutes=1))

        response = self.client.get('/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что в списке только 1 привычка (своя), а не 2
        # (С учетом пагинации данные лежат в ключе 'results')
        self.assertEqual(len(response.json()['results']), 1)
