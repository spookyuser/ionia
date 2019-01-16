# pylint: skip-file
import pytest
from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key
import time
from django.db import connection
import fity3
from ionia.models import CommonInfo
from user.models import User
from island.models import Island
from post.models import Post

""""Setup for testing abstract models.

See-Also: https://medium.com/@nazrulworld/testing-abstract-model-in-django-df6e59bdd7a6
"""


class CommonInfoImplementation(CommonInfo):
    class Meta:
        app_label = "test"
        db_table = "test_table"


class Now(object):
    """Setup for testing snowflake id
    If we use the get_id method from the class it can't generate true ids
    fast enough
    """

    def __init__(self, now):
        self.now = now
        self.log = []

    def __call__(self):
        return self.now

    def sleep(self, n):
        self.log.append(n)
        self.now += n
        return self

    def clear(self):
        self.log = []


class Generator:
    @staticmethod
    def get_generator():
        now = Now(1413401558001)
        return fity3.generator(1, sleep=now.sleep, now=now)

    @staticmethod
    def get_id(generator):
        print("Got ID!")
        return next(generator)


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        generator = Generator.get_generator()

        with connection.schema_editor(atomic=True) as schema_editor:
            schema_editor.create_model(CommonInfoImplementation)

        for index in range(0, 2):
            CommonInfoImplementation.objects.create(id=Generator.get_id(generator))

        user = User.objects.create_user(
            id=Generator.get_id(generator),
            username="test",
            email="test@email.com",
            password="test",
        )

        island = Island.objects.create(
            id=Generator.get_id(generator), created_by=user, name="test"
        )

        for index in range(0, 260):
            Post.objects.create(
                id=Generator.get_id(generator),
                user=user,
                island=island,
                post=str(index) + "_post",
            )

