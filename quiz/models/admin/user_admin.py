from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "is_staff", "display_groups")

    def display_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
