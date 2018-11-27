import datetime
import pytest

from ..models import CommonInfo
from .conftest import CommonInfoImplementation


@pytest.mark.django_db
class TestCommonInfo:
    def test_generates_id(self):
        common_info = CommonInfoImplementation.objects.first()
        assert common_info.id

    def test_id_is_sequential(self):
        first = CommonInfoImplementation.objects.all()[0]
        second = CommonInfoImplementation.objects.all()[1]
        assert first.id < second.id

    def test_ordering(self):
        ordering = CommonInfo._meta.ordering
        print(ordering)
        assert ordering[0] == "-id"

    def test_created_at(self):
        now = datetime.datetime.now()
        common_info = CommonInfoImplementation.objects.first()
        delta = now - common_info.created_at()
        assert delta.microseconds > 0
