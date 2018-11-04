from django.db import models
from django.db.models import Count
from django.contrib.postgres.fields import citext
from ionia.models import CommonInfo
from user.models import User


class Island(CommonInfo):
    """A set of posts

    From CommonInfo we get:
        Snowflake id
        created_at derived by snowflake
    """

    name = citext.CICharField(max_length=20, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=140, blank=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_island(name):
        return Island.objects.get(name__iexact=name)

    @staticmethod
    def get_top_islands(top=5):
        return (
            Island.objects.all()
            .annotate(subscribers=Count("subscribed_by"))
            .order_by("-subscribers")[:top]
        )

    @staticmethod
    def get_my_islands(user):
        """Islands user subscribes to"""
        return Island.objects.filter(subscribed_by=user)

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("island:detail", args=[self.name])
