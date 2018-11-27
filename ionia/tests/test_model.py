import datetime
import pytest

from .conftest import CommonInfoImplementation


@pytest.mark.django_db
class TestCommonInfo:
    def test_generates_id(self):
        assert CommonInfoImplementation.objects.first().id

    def test_id_is_sequential(self):
        assert (
            CommonInfoImplementation.objects.all()[0].id
            < CommonInfoImplementation.objects.all()[1].id
        )

    def test_created_at(self):
        assert (
            datetime.datetime.now()
            - CommonInfoImplementation.objects.first().created_at()
        )
