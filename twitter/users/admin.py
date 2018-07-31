from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from .models import User

from twitter.users.forms import MyUserChangeForm, UserCreationForm


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = MyUserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("full_name", "followers")}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "full_name", "is_superuser"]
    search_fields = ["username"]
