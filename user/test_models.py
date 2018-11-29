import pytest
from django.db import IntegrityError
from django.core import mail
from .models import User


@pytest.fixture(autouse=True)
def email_backend_setup(settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"



@pytest.mark.django_db
class TestUser:

    def test_username_label(self):
        """From https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing#Models"""
        user = User.objects.first()
        field_label = user._meta.get_field("username").verbose_name
        assert field_label == "username"

    def test_follows_label(self):
        user = User.objects.first()
        field_label = user._meta.get_field("follows").verbose_name
        assert field_label == "follows"

    def test_subscribes_label(self):
        user = User.objects.first()
        field_label = user._meta.get_field("subscribes").verbose_name
        assert field_label == "subscribes"

    def test_likes_label(self):
        user = User.objects.first()
        field_label = user._meta.get_field("likes").verbose_name
        assert field_label == "likes"

    def test_email_label(self):
        user = User.objects.first()
        field_label = user._meta.get_field("email").verbose_name
        assert field_label == "email address"

    def test_is_staff_label(self):
        user = User.objects.first()
        field_label = user._meta.get_field("is_staff").verbose_name
        assert field_label == "staff status"

    def test_is_active_label(self):
        user = User.objects.first()
        field_label = user._meta.get_field("is_active").verbose_name
        assert field_label == "active"

    def test_user_label(self):
        user = User.objects.first()
        user_label = user._meta.verbose_name_raw
        assert user_label == "user"

    def test_email_is_optional(self):
        user = User.objects.create_user(username="test_2", password="test")
        assert user

    def test_email_sends(self):
        user = User.objects.get_by_natural_key("test")
        user.email_user("subject", "message", "from@email.com")
        assert len(mail.outbox) == 1

    def test_username_max_length(self):
        user = User.objects.first()
        max_length = user._meta.get_field("username").max_length
        assert max_length == 20

    def test_username_is_unique(self):
        with pytest.raises(IntegrityError):
            User.objects.create_user(username="test", password="test")

    def test_email_is_unique(self):
        with pytest.raises(IntegrityError):
            User.objects.create_user("test_3", "test@email.com", "test")

    def test_multiple_users_can_have_no_email(self):
        try:
            User.objects.create_user(username="test_4", password="test")
            User.objects.create_user(username="test_5", password="test")
        except IntegrityError:
            raise pytest.fail("Raised {0}".format(IntegrityError))
