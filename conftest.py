# pylint: skip-file
import pytest
import time
from django.db import connection

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


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        with connection.schema_editor(atomic=True) as schema_editor:
            schema_editor.create_model(CommonInfoImplementation)
        for _ in range(0, 2):
            time.sleep(0.1)
            CommonInfoImplementation.objects.create()
        user = User.objects.create_user("test", "test@email.com", "test")
        island = Island.objects.create(created_by=user, name="test")
        Post.objects.create(post="test", user=user, island=island)

        test_island = Island.objects.create(name="test_island", created_by=user)
        time.sleep(0.1)
        test_island_2 = Island.objects.create(name="test_island_2", created_by=user)

        Post.objects.create(post="test_post", user=user, island=test_island)
        time.sleep(0.1)
        Post.objects.create(post="test_post_2", user=user, island=test_island_2)

