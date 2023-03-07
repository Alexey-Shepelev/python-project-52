from django.contrib import admin
from .models import LocalUser


@admin.register(LocalUser)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['username']
    list_display = (
        'id',
        'first_name',
        'last_name',
        'username',
        'date_joined',
        'password'
    )
