from django.db import models

from ionia.models import CommonInfo
from island.models import Island
from post.sorts import New, Hot
from user.models import User

hot = Hot()


class Post(CommonInfo):
    """A limited character paragraph"""
    post = models.CharField(max_length=240)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    island = models.ForeignKey(Island, on_delete=models.CASCADE)

    def __str__(self):
        return self.post

    @staticmethod
    def list_types():
        """The different ways you can view posts

        Either by subscription (which islands you subscribe to)
        Or follow (which users you follow)
        """
        return ["subscribed", "following"]

    @staticmethod
    def get_user_posts(list_type, sort, user):
        """Given a list type and sort method, show a user the posts for that list type and sort

        Possible combinations:
            Subscribed + Hot
            Subscribed + New
            Following + Hot
            Following + New
        Defaults to Subscribed + Hot

        After finding posts by the list type, filter based on sort
        """
        if list_type == "subscribed":
            posts = Post.objects.filter(island__subscribed_by=user)
        elif list_type == "following":
            posts = Post.objects.filter(user__followed_by=user)
        else:
            posts = Post.objects.filter(island__subscribed_by=user)

        return Post.sort_posts(sort, posts)

    @staticmethod
    def get_island_posts(sort, island):
        """Get posts given an island"""
        posts = Post.objects.filter(island=island)
        return Post.sort_posts(sort, posts)

    @staticmethod
    def get_anonymous_posts(sort):
        """Get posts for an anonymous user (no filter)"""
        posts = Post.objects.all()
        return Post.sort_posts(sort, posts)

    @staticmethod
    def sort_posts(sort, posts, consider=1000):
        """After filtering posts by a list type, sort them by a sort type

        Defaults to Hot
        """
        if sort == New.name:
            return posts.order_by("-id")[:consider]
        else:
            return hot.order_by(posts)[:consider]
