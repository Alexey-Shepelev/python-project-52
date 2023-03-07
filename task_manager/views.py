from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.contrib import messages


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    success_message = _('You are logged in')


def user_logout(request):
    logout(request)
    messages.info(request, _('You are logged out'))
    return redirect('index')

# class UserLogoutView(LogoutView):
#
#     def dispatch(self, request, *args, **kwargs):
#         response = super().dispatch(request, *args, **kwargs)
#         messages.info(request, _('You are logged out'))
#         return response
