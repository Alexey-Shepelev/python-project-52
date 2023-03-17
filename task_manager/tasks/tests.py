from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models import ProtectedError
from .models import Task


class TaskAppTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json']
    test_task = {
        'name': 'test',
        'description': '',
        'status': 1,
        'executor': ''
    }

    def setUp(self) -> None:
        self.guest = Client()

        self.user = get_user_model().objects.first()
        self.auth_user = Client()
        self.auth_user.force_login(self.user)

    def test_unauth_access(self):
        response = self.guest.get(reverse('tasks:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        response = self.guest.get(reverse('tasks:create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        response = self.guest.get(reverse('tasks:update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        response = self.guest.get(reverse('tasks:delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_task_view(self):
        # list of tasks
        response = self.auth_user.get(reverse('tasks:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks/index.html')
        # chosen task page view
        response = self.auth_user.get(reverse('tasks:detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, template_name='tasks/task_detail.html')

    def test_task_create(self):
        response = self.auth_user.get(reverse('tasks:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks/create.html')

        response = self.auth_user.post(reverse('tasks:create'), self.test_task)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks:index'))
        self.assertEqual(Task.objects.last().name, 'test')
        self.assertEqual(Task.objects.count(), 4)

    def test_task_update(self):

        self.assertEqual(Task.objects.get(pk=1).name, 'task1')

        response = self.auth_user.get(
            reverse('tasks:update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks/update.html')

        response = self.auth_user.post(
            reverse('tasks:update', kwargs={'pk': 1}), self.test_task)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks:index'))
        self.assertEqual(Task.objects.get(pk=1).name, 'test')

    def test_task_delete(self):

        self.assertEqual(Task.objects.count(), 3)
        # try to "get" by not author
        response = self.auth_user.get(
            reverse('tasks:delete', kwargs={'pk': 1}))
        self.assertRaises(ProtectedError)
        self.assertTemplateNotUsed(response, template_name='tasks/delete.html')
        # try to delete by author
        self.client.force_login(get_user_model().objects.get(pk=2))
        response = self.client.get(
            reverse('tasks:delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks/delete.html')
        response = self.client.post(
            reverse('tasks:delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks:index'))
        self.assertEqual(Task.objects.count(), 2)
        self.assertFalse(Task.objects.filter(pk=1))
