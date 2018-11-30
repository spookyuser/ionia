from django.db import models
import pytest

from .models import Post


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

