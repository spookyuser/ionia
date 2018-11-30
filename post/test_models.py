from django.db import models
import pytest

from .models import Post
from island.models import Island
from user.models import User
import time


@pytest.mark.django_db
class TestPost:

    # post = models.CharField(max_length=240)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # island = models.ForeignKey(Island, on_delete=models.CASCADE)

    def test_post_label(self):
        post = Post.objects.first()
        field_label = post._meta.get_field("post").verbose_name
        assert field_label == "post"

    def test_user_label(self):
        post = Post.objects.first()
        field_label = post._meta.get_field("user").verbose_name
        assert field_label == "user"

    def test_island_label(self):
        post = Post.objects.first()
        field_label = post._meta.get_field("island").verbose_name
        assert field_label == "island"

    def test_post_max_length(self):
        post = Post.objects.first()
        field_max_length = post._meta.get_field("post").max_length
        assert field_max_length == 240

    def test_post_string(self):
        post = Post.objects.first()
        assert post.__str__() == post.post

    def test_list_types_returns_list(self):
        list_types = Post.list_types()
        assert isinstance(list_types, list)

    def test_list_types_returns_at_least_one_type(self):
        list_types = Post.list_types()
        assert list_types

    def test_get_user_posts_default(self):
        user = User.objects.first()

        test_island = Island.objects.create(name="test_island", created_by=user)
        time.sleep(0.1)
        test_island_2 = Island.objects.create(name="test_island_2", created_by=user)

        Post.objects.create(post="test_post", user=user, island=test_island)
        time.sleep(0.1)
        Post.objects.create(post="test_post_2", user=user, island=test_island_2)

        user_posts = Post.get_user_posts(list_type=None, sort=None, user=user)
        for post in user_posts:
            assert user in post.island.subscribed_by

