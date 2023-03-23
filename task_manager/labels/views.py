from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import Label
from .forms import LabelForm
from task_manager.permissions import MyLoginRequiredMixin, MyDeleteView
from django.utils.translation import gettext_lazy as _


class IndexView(MyLoginRequiredMixin, ListView):
    model = Label
    context_object_name = 'labels'
    template_name = 'labels/index.html'


class LabelCreateView(MyLoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels:index')
    success_message = _('Label successfully created')


class LabelUpdateView(MyLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels:index')
    success_message = _('Label successfully updated')


class LabelDeleteView(MyLoginRequiredMixin, MyDeleteView):
    model = Label
    success_url = reverse_lazy('labels:index')
    template_name = 'labels/delete.html'
    message_success = _('Label successfully deleted')
    message_protect = _('Cannot delete label because it in use')
