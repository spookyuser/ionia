from .models import Island
from user.models import User
from django.db import IntegrityError
from django.db.models import Count

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

    def test_name_max_length(self):
        island = Island.objects.first()
        max_length = island._meta.get_field("name").max_length
        assert max_length == 20

    def test_description_max_length(self):
        island = Island.objects.first()
        max_length = island._meta.get_field("description").max_length
        assert max_length == 140

    def test_name_is_unique(self):
        island = Island.objects.first()
        with pytest.raises(IntegrityError):
            Island.objects.create(name=island.name, created_by=island.created_by)

    def test_island_string(self):
        island = Island.objects.first()
        string = island.__str__()
        assert string == island.name

    def test_get_island_is_case_insensitive(self):
        island = Island.objects.first()
        found_island = Island.get_island(island.name.upper())
        assert island == found_island

    def test_get_top_islands_returns_5(self):
        top_islands = Island.get_top_islands()
        assert len(top_islands) <= 5

    def test_get_top_islands_counts_by_subscribers(self):
        top_islands = Island.get_top_islands()
        for index, island in enumerate(top_islands):
            if index is not 0:
                assert (
                    island.subscribed_by.count()
                    >= top_islands[index - 1].subscribed_by.count()
                )

    def test_get_my_islands_returns_subscriptions(self):
        user = User.objects.first()
        my_islands = Island.get_my_islands(user)
        for island in my_islands:
            assert user in island.subscribed_by

    def test_absolute_url(self):
        island = Island.objects.first()
        absolute_url = island.get_absolute_url()
        assert absolute_url == ("/i/" + island.name + "/")
