# Stdlib imports
# Core Django imports
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.postgres.fields import CICharField, CIEmailField
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Third-party app imports
# Imports from my apps


class User(AbstractBaseUser, PermissionsMixin):
    """Default user for weathervis.

    An custom user class base implementing a fully featured User model with
    admin-compliant permissions.
    Username, email and password are required. Other fields are optional.

    based on class AbstractUser
    see https://github.com/django/django/blob/main/django/contrib/auth/models.py
    """

    #: First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    username_validator = ASCIIUsernameValidator()

    username = CICharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only. Case insensitive."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    email = CIEmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email address already exists."),
        },
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
        ),
    )

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]  # USERNAME_FIELD & Password are required by default.

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, val):
        return setattr(self, key, val)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self) -> str:
        """
        Return the first_name plus the last_name, with a space in between.
        """
        # full_name = "%s %s" % (self.first_name, self.last_name)
        full_name = f"{self.name}".strip()
        if not full_name:
            full_name = None
        return full_name

    def get_short_name(self) -> str:
        """Return the short name for the user.

        Assumed as the first word of the name.
        """
        # return self.first_name
        # name_list = "%s" % (self.name.split())
        # return name_list[0] if name_list else None
        name_list = self.name.split()
        # return "%s" % (next(iter(name_list), ""))
        return next(iter(name_list), None)

    def email_user(self, subject: str, message: str, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
