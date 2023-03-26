from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models import ProtectedError


# from django.utils.translation import gettext_lazy as _


class UsersAppTest(TestCase):
    fixtures = ['users.json', 'tasks.json', 'statuses.json', 'labels.json']

    def setUp(self) -> None:
        self.guest = Client()

        self.user = get_user_model().objects.first()
        self.auth_user = Client()
        self.auth_user.force_login(self.user)

    def test_user_create(self):
        response = self.guest.get(reverse('users:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/create.html')

        response = self.guest.post(reverse('users:create'),
                                   {'first_name': 'user',
                                    'last_name': 'test',
                                    'username': 'tester',
                                    'password1': '1234',
                                    'password2': '1234'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        user = get_user_model().objects.last()
        self.assertEqual(user.username, 'tester')

        response = self.guest.get(reverse('users:index'))
        self.assertEqual(get_user_model().objects.count(), 4)

    def test_user_update(self):
        # not logged in user
        response = self.guest.get(reverse('users:update', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        # other user
        response = self.auth_user.get(reverse('users:update', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:index'))

        # authorized user
        self.assertEqual(self.user.username, 'sailor')
        response = self.auth_user.get(reverse('users:update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/update.html')
        response = self.auth_user.post(reverse('users:update',
                                               kwargs={'pk': self.user.id}),
                                       {'first_name': 'newname',
                                        'last_name': 'newname',
                                        'username': 'new',
                                        'password1': '1234',
                                        'password2': '1234'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:index'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'new')

    def test_user_delete(self):
        # not logged in user
        response = self.guest.get(reverse('users:delete', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        # other user
        response = self.auth_user.get(reverse('users:delete', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:index'))
        self.assertTrue(get_user_model().objects.filter(pk=3))

        # authorized user
        response = self.auth_user.get(reverse('users:delete',
                                              kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/delete.html')
        # authorized user without task
        response = self.auth_user.post(reverse('users:delete',
                                               kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:index'))
        self.assertEqual(get_user_model().objects.count(), 2)
        # authorized user with task
        self.client.force_login(get_user_model().objects.get(pk=2))
        response = self.client.post(reverse('users:delete',
                                            kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:index'))
        self.assertRaises(ProtectedError)
        self.assertTrue(get_user_model().objects.filter(pk=2))
