import datetime

import pytest
from django.db import IntegrityError

from .models import CommonInfo, get_id
from conftest import CommonInfoImplementation


@pytest.mark.django_db
class TestCommonInfo:
    def test_generates_id_in_abstract(self):
        common_info_id = get_id()
        assert common_info_id

    def test_generates_id_in_model(self):
        common_info = CommonInfoImplementation.objects.first()
        assert common_info.id

    def test_id_is_sequential(self):
        first = CommonInfoImplementation.objects.all()[0]
        second = CommonInfoImplementation.objects.all()[1]
        assert first.id < second.id

    def test_id_is_unique(self):
        common_info = CommonInfoImplementation.objects.create()
        with pytest.raises(IntegrityError):
            CommonInfoImplementation.objects.create(id=common_info.id)

    def test_order_by_reverse_id(self):
        ordering = CommonInfo._meta.ordering
        print(ordering)
        assert ordering[0] == "-id"

    def test_created_at_is_date(self):
        now = datetime.datetime.now()
        common_info = CommonInfoImplementation.objects.first()
        delta = now - common_info.created_at()
        assert delta.microseconds > 0
