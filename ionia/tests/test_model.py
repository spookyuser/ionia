import pytest
from .conftest import CommonInfoImplementation


@pytest.mark.django_db
def test_generates_id():
    CommonInfoImplementation.objects.create()
    assert CommonInfoImplementation.objects.first().id