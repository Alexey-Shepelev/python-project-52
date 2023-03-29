from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import test


@test.modify_settings(MIDDLEWARE={'remove': [
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware']})
class AppTest(TestCase):
    fixtures = ['users.json']

    def setUp(self) -> None:
        self.guest = Client()

        self.user = get_user_model().objects.first()
        self.auth_user = Client()
        self.auth_user.force_login(self.user)

    def test_index_page(self):
        response = self.guest.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='index.html')

    def test_users_page(self):
        response = self.guest.get(reverse('users:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/index.html')
        self.assertEqual(get_user_model().objects.count(), 3)
        self.assertNotContains(response, text=_('Statuses'))
        self.assertNotContains(response, text=_('Labels'))
        self.assertNotContains(response, text=_('Tasks'))

        response = self.auth_user.get(reverse('users:index'))
        self.assertContains(response, text=_('Statuses'))
        self.assertContains(response, text=_('Labels'))
        self.assertContains(response, text=_('Tasks'))
