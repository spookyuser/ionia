from django.db import models
import pytest

from .models import Post
from island.models import Island
from user.models import User


@pytest.mark.django_db
class TestPost:
    def test_string(self):
        # post = Post.objects.first()
        # assert post.__str__() == post.post
        User.objects.first()
