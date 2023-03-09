from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import Status
from .forms import StatusForm
from task_manager.permissions import MyLoginRequiredMixin
from django.utils.translation import gettext_lazy as _


class IndexView(MyLoginRequiredMixin, ListView):
    model = Status
    context_object_name = 'statuses'
    template_name = 'statuses/index.html'


class StatusCreateView(MyLoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = StatusForm
    success_url = reverse_lazy('statuses:index')
    template_name = 'statuses/create.html'
    success_message = _('Status successfully created')


class StatusUpdateView(MyLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('statuses:index')
    template_name = 'statuses/update.html'
    success_message = _('Status successfully updated')


class StatusDeleteView(MyLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    success_url = reverse_lazy('statuses:index')
    template_name = 'statuses/delete.html'
    success_message = _('Status successfully deleted')
