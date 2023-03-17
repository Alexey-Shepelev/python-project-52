from django.views.generic import (
    ListView, CreateView, DetailView, UpdateView, DeleteView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm
from task_manager.permissions import MyLoginRequiredMixin, TaskPermissionMixin
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.shortcuts import redirect


class IndexView(MyLoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/index.html'


class TaskCreateView(MyLoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = TaskForm
    success_url = reverse_lazy('tasks:index')
    template_name = 'tasks/create.html'
    success_message = _('Task successfully created')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TaskView(MyLoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'


class TaskUpdateView(MyLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks:index')
    template_name = 'tasks/update.html'
    success_message = _('Task successfully updated')


class TaskDeleteView(MyLoginRequiredMixin, TaskPermissionMixin,
                     SuccessMessageMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks:index')
    template_name = 'tasks/delete.html'
    success_message = _('Task successfully deleted')


