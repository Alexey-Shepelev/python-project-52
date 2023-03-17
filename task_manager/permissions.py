from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.views.generic import DeleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _


class MyLoginRequiredMixin(LoginRequiredMixin):

    def handle_no_permission(self):
        messages.error(
            self.request, _('You are not authorized! Please sign in.'))
        return redirect(reverse_lazy('login'))


class UserPermissionMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if self.request.user != self.get_object():
            messages.error(request, _(
                "You don't have permissions to change another user."))
            return redirect(reverse_lazy('users:index'))

        return super().dispatch(request, *args, **kwargs)


class TaskPermissionMixin(AccessMixin):
    success_url = ''

    def dispatch(self, request, *args, **kwargs):
        if request.user != self.get_object().creator:
            messages.error(request,
                           _('The task can only be deleted by its author.'))
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)


class MyDeleteView(DeleteView):
    message_success = ''
    message_protect = ''

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.message_protect)
        else:
            messages.success(request, self.message_success)
        return redirect(self.get_success_url())
