from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
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
