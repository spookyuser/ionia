import pytest
from django.db import IntegrityError

from .models import User


@pytest.fixture(scope="module")
def user_fixture(django_db_blocker):
    with django_db_blocker.unblock():
        User.objects.create_user("test", "test@email.com", "test")


@pytest.mark.usefixtures("user_fixture")
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

    def test_user_already_exists(self):
        with pytest.raises(IntegrityError):
            User.objects.create_user("test", "test@email.com", "test")

    def test_user_with_null_email(self):
        User.objects.create_user(username="test_2", password="test")
