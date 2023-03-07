from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from .models import LocalUser
from .forms import UserForm
from task_manager.permissions import MyLoginRequiredMixin, UserPermissionMixin


class IndexView(ListView):
    model = LocalUser
    context_object_name = 'users'
    template_name = 'users/index.html'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = LocalUser
    form_class = UserForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = _('User created successfully')


class UserUpdateView(MyLoginRequiredMixin, UserPermissionMixin,
                     SuccessMessageMixin, UpdateView):
    model = LocalUser
    form_class = UserForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:index')
    success_message = _('User updated successfully')


class UserDeleteView(MyLoginRequiredMixin, UserPermissionMixin,
                     SuccessMessageMixin, DeleteView):
    model = LocalUser
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:index')
    success_message = _('User successfully deleted')
