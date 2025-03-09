from django.test import TestCase
from django.urls import reverse
from users.models import User


class RegisterViewTest(TestCase):
    def setUp(self):
        # Данные для теста регистрации
        self.valid_data = {
            'email': 'testuser@example.com',
            'full_name': 'Иван Иванов',
            'phone_number': '+79991234567',
            'address': 'ул. Ленина, д. 1',
            'region': 'Москва',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
        }

        self.invalid_data = {
            'email': 'testuser@example.com',
            'full_name': 'Иван Иванов123',  # Некорректное ФИО
            'phone_number': '12345',  # Некорректный номер
            'address': 'ул. Ленина, д. 1',
            'region': 'Москва',
            'password1': 'TestPassword123!',
            'password2': 'AnotherPassword123!',  # Пароли не совпадают
        }

    def test_register_valid_data(self):
        """Тест успешной регистрации с корректными данными"""
        response = self.client.post(reverse('users:register'), self.valid_data)
        self.assertEqual(response.status_code, 302)  # Ожидаем редирект
        self.assertTrue(User.objects.filter(email=self.valid_data['email']).exists())

    def test_register_invalid_data(self):
        """Тест неудачной регистрации с некорректными данными"""
        # Отправляем POST-запрос
        response = self.client.post(reverse('users:register'), self.invalid_data)

        # Проверяем, что форма вернулась с ошибкой
        self.assertEqual(response.status_code, 200)  # Остаёмся на той же странице
        self.assertContains(response, 'Номер телефона может содержать только цифры')  # Проверяем текст ошибки

        # Проверяем ошибки формы через контекст
        form = response.context['form']
        self.assertTrue(form.errors)  # Форма должна содержать ошибки
        self.assertIn('phone_number', form.errors)  # Ошибка должна быть связана с полем 'phone_number'
        self.assertIn('Номер телефона может содержать только цифры', form.errors['phone_number'])
