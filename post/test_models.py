from django.db import models
import pytest

from .models import Post
from model_mommy import mommy
from island.models import Island
from user.models import User
import time
from post.sorts import New, Hot


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

    def test_get_user_posts_default_returns_subscribed(self):
        user = User.objects.first()
        user_posts = Post.get_user_posts(list_type=None, sort=None, user=user)
        for post in user_posts:
            assert user in post.island.subscribed_by

    def test_get_user_posts_subscribed_returns_subscribed(self):
        user = User.objects.first()
        user_posts = Post.get_user_posts(list_type="subscribed", sort=None, user=user)
        for post in user_posts:
            assert user in post.island.subscribed_by

    def test_get_user_posts_following_returns_following(self):
        user = User.objects.first()
        user_posts = Post.get_user_posts(list_type="following", sort=None, user=user)
        for post in user_posts:
            assert user in post.user.followed_by

    def test_get_island_posts_returns_island_posts(self):
        island = Island.objects.first()
        island_posts = mommy.make("post.Post", island=island, _quantity=10)
        for post in island_posts:
            assert post.island == island

    def test_get_anonymous_posts_returns_all_posts(self):
        all_posts = Post.objects.all()
        anonymous_posts = Post.get_anonymous_posts(sort=None)
        assert len(all_posts) == len(anonymous_posts)

    def test_sort_posts_by_hot_returns_hot(self):
        hot = Hot()
        posts = Post.objects.all()
        sorted_posts = Post.sort_posts(sort=hot.name, posts=posts)
        hot_sorted_posts = hot.order_by(posts)
        for index, post in enumerate(sorted_posts):
            assert hot_sorted_posts[index].id == post.id

    def test_sort_posts_by_new_returns_new(self):
        new = New()
        posts = Post.objects.all()
        sorted_posts = Post.sort_posts(sort=new.name, posts=posts)
        new_sorted_posts = posts.order_by("-id")
        for index, post in enumerate(sorted_posts):
            assert new_sorted_posts[index].id == post.id

