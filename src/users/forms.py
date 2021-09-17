# Stdlib imports
# Core Django imports
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model

# Third-party app imports
# Imports from my apps

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("username", "email")
