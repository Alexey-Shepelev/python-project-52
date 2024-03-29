from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Status
from django.db.models import ProtectedError
from django import test


@test.modify_settings(MIDDLEWARE={'remove': [
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware']})
class StatusAppTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json', 'labels.json']

    def setUp(self):
        self.guest = Client()

        self.user = get_user_model().objects.first()
        self.auth_user = Client()
        self.auth_user.force_login(self.user)

    def test_unauth_access(self):
        # unauthorized users cannot get access to Statuses and
        # should be redirected to login page
        response = self.guest.get(reverse('statuses:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        response = self.guest.get(reverse('statuses:create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        response = self.guest.get(reverse('statuses:update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        response = self.guest.get(reverse('statuses:delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_status_create(self):
        response = self.auth_user.get(reverse('statuses:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='statuses/create.html')

        response = self.auth_user.post(reverse('statuses:create'),
                                       {'name': 'test'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses:index'))
        self.assertEqual(Status.objects.last().name, 'test')
        self.assertEqual(Status.objects.count(), 5)

    def test_status_update(self):

        self.assertEqual(Status.objects.get(pk=1).name, 'новый')

        response = self.auth_user.get(
            reverse('statuses:update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='statuses/update.html')

        response = self.auth_user.post(
            reverse('statuses:update', kwargs={'pk': 1}), {'name': 'test'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses:index'))
        self.assertEqual(Status.objects.get(pk=1).name, 'test')

    def test_status_delete(self):
        self.assertEqual(Status.objects.count(), 4)
        response = self.auth_user.get(
            reverse('statuses:delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='statuses/delete.html')

        # try to remove status in use
        response = self.auth_user.post(
            reverse('statuses:delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses:index'))
        self.assertRaises(ProtectedError)
        self.assertEqual(Status.objects.count(), 4)
        self.assertTrue(Status.objects.filter(pk=1))

        # try to remove status not in use
        response = self.auth_user.post(
            reverse('statuses:delete', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses:index'))
        self.assertEqual(Status.objects.count(), 3)
        self.assertFalse(Status.objects.filter(pk=2))
