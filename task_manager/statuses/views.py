from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import Status
from .forms import StatusForm
from task_manager.permissions import MyLoginRequiredMixin, MyDeleteView
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


class StatusDeleteView(MyLoginRequiredMixin, MyDeleteView):
    model = Status
    success_url = reverse_lazy('statuses:index')
    template_name = 'statuses/delete.html'
    message_success = _('Status successfully deleted')
    message_protect = _('Cannot delete status because it in use')
