from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Label
from django.db.models import ProtectedError
from django import test


@test.modify_settings(MIDDLEWARE={'remove': [
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware']})
class LabelAppTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json', 'labels.json']

    def setUp(self) -> None:
        self.guest = Client()

        self.user = get_user_model().objects.first()
        self.auth_user = Client()
        self.auth_user.force_login(self.user)

    def test_unauth_access(self):
        # unauthorized users cannot get access to Labels and
        # should be redirected to login page
        response = self.guest.get(reverse('labels:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        response = self.guest.get(reverse('labels:create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        response = self.guest.get(reverse('labels:update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        response = self.guest.get(reverse('labels:delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_status_create(self):
        response = self.auth_user.get(reverse('labels:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='labels/create.html')

        response = self.auth_user.post(reverse('labels:create'),
                                       {'name': 'test'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels:index'))
        self.assertEqual(Label.objects.last().name, 'test')
        self.assertEqual(Label.objects.count(), 4)

    def test_status_update(self):

        self.assertEqual(Label.objects.get(pk=1).name, 'label1')

        response = self.auth_user.get(
            reverse('labels:update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='labels/update.html')

        response = self.auth_user.post(
            reverse('labels:update', kwargs={'pk': 1}), {'name': 'test'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels:index'))
        self.assertEqual(Label.objects.get(pk=1).name, 'test')

    def test_status_delete(self):
        self.assertEqual(Label.objects.count(), 3)
        response = self.auth_user.get(
            reverse('labels:delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='labels/delete.html')

        # try to remove label in use
        response = self.auth_user.post(
            reverse('labels:delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels:index'))
        self.assertRaises(ProtectedError)
        self.assertEqual(Label.objects.count(), 3)
        self.assertTrue(Label.objects.filter(pk=1))

        # try to remove label not in use
        response = self.auth_user.post(
            reverse('labels:delete', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels:index'))
        self.assertEqual(Label.objects.count(), 2)
        self.assertFalse(Label.objects.filter(pk=3))
