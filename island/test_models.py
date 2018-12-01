from .models import Island
import pytest


@pytest.mark.django_db
class TestIsland:
    def test_name_label(self):
        island = Island.objects.first()
        field_label = island._meta.get_field("name").verbose_name
        assert field_label == "name"

    def test_created_by_label(self):
        island = Island.objects.first()
        field_label = island._meta.get_field("created_by").verbose_name
        assert field_label == "created by"

    def test_description_label(self):
        island = Island.objects.first()
        field_label = island._meta.get_field("description").verbose_name
        assert field_label == "description"
