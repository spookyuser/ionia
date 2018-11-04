from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.postgres.fields import citext
from ionia.extras import EmailNullField
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _

from ionia.models import CommonInfo


class UserManager(BaseUserManager):
    """Override base django user manager

    No changes but allows for customisation down the road.
    """
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """Create and save a user with the given username, email, and password."""
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(username__iexact=username)


class User(AbstractBaseUser, PermissionsMixin, CommonInfo):
    """An abstract base class implementing a fully featured User model with admin-compliant permissions.

    Username and password are required. Other fields are optional.

    From original django Abstract User, to allow for customisation.
    Changes:
        No fullname/first name/last name.
        Implements Common Info, so we have get a snowflake id.
        No date joined, we get this from the snowflake id.
        This class is not an Abstract class so it can be used without a wrapper class.
    """

    username_validator = UnicodeUsernameValidator()

    username = citext.CICharField(
        _("username"),
        max_length=20,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={"unique": _("A user with that username already exists.")},
    )
    follows = models.ManyToManyField("user.User", related_name="followed_by")
    subscribes = models.ManyToManyField("island.Island", related_name="subscribed_by")
    likes = models.ManyToManyField("post.Post", related_name="liked_by")
    email = EmailNullField(
        _("email address"),
        blank=True,
        null=True,
        unique=True,
        error_messages={"unique": _("An user with that email already exists.")},
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
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an  email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
