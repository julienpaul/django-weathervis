# Stdlib imports
# Core Django imports
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

# Third-party app imports
# Imports from my apps
from src.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "name",
                    "email",
                    "bio",
                    "organisation",
                )
            },
        ),
        (_("Groups"), {"fields": ("groups",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    # limit staff fieldsets to prevent escalation
    # https://stackoverflow.com/a/43128444
    staff_fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        # Keeping the group parts? Ok, but they shouldn't be able to define
        # their own groups, up to you...
        (_("Groups"), {"fields": ("groups",)}),
        # Removing the permission part
        # (_('Permissions'), {'fields': ('is_staff', 'is_active', 'is_superuser', 'user_permissions')}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    staff_readonly_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "last_login",
        "date_joined",
    )
    list_display = [
        "username",
        "name",
        "is_active",
        "is_staff",
        "is_superuser",
    ]
    list_filter = [
        "groups",
    ]
    search_fields = ["name"]

    def get_fieldsets(self, request, obj=None):
        if not request.user.is_superuser:
            return self.staff_fieldsets
        else:
            return super(UserAdmin, self).get_fieldsets(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return self.staff_readonly_fields
        else:
            return super(UserAdmin, self).get_readonly_fields(request, obj)

    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            # staff user can not see other Staff member or superuser
            return qs.filter(~Q(groups__name="Staff") & ~Q(is_superuser=True))
        return qs
