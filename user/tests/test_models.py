from ..models import User
import pytest
from django.db import IntegrityError


@pytest.mark.django_db
class TestUser:
    def test_create_user(self):
        User.objects.create_user("test", "test@gmail.com", "test")

    def test_user_already_exists(self):
        User.objects.create_user("test", "test@gmail.com", "test")
        with pytest.raises(IntegrityError):
            User.objects.create_user("test", "test@gmail.com", "test")

    def test_user_null_email(self):
        User.objects.create_user(username="test", password="test")
    
