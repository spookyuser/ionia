import pytest
from django.core.management import call_command
from django.db import connection, models

from ..models import CommonInfo

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
