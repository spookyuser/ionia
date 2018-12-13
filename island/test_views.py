import pytest
from island.models import Island
import time
from user.models import User
from model_mommy import mommy
from django.urls import reverse

"""From https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing#Views"""

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def disable_axes(settings):
    if "axes" in settings.INSTALLED_APPS:
        settings.AUTHENTICATION_BACKENDS.remove("axes.backends.AxesModelBackend")
        settings.INSTALLED_APPS.remove("axes")


class TestIslandListView:
    def test_view_exists_at_desired_location(self, client):
        response = client.get("/islands/")
        assert response.status_code == 200

    def test_view_accessible_by_name(self, client):
        response = client.get(reverse("island:list"))
        assert response.status_code == 200


class TestIslandCreateView:
    def test_redirect_if_not_logged_in(self, client):
        response = client.get(reverse("island:create"))
        assert (
            response.status_code == 302
            and response.url == "/users/login/?next=/island/create/"
        )

    def test_view_exists_at_desired_location(self, client):
        client.login(username="test", password="test")
        response = client.get("/island/create/")
        assert response.status_code == 200

    def test_view_accessible_by_name(self, client):
        client.login(username="test", password="test")
        response = client.get(reverse("island:create"))
        assert response.status_code == 200

    def test_create_view_subscribes_user(self, client):
        client.login(username="test", password="test")
        client.post(reverse("island:create"), {"name": "test_create_island"})
        island = Island.objects.get(name="test_create_island")
        assert island.created_by in island.subscribed_by.all()


class TestIslandChangeSubscribe:
    def test_redirect_if_not_logged_in(self, client):
        response = client.get(
            reverse("island:change_subscribe", args=["test_island", "subscribe"])
        )
        assert response.status_code == 302 and response.url == (
            "/users/login/?next=/i/" + "test_island" + "/subscribe/subscribe/"
        )

    def test_accessible_by_name(self, client):
        client.login(username="test", password="test")
        island = Island.objects.first()
        response = client.get(
            reverse("island:change_subscribe", args=[island.name, "subscribe"])
        )
        assert response.status_code == 302 and response.url == "/i/" + island.name + "/"

    def test_exists_at_desired_location(self, client):
        client.login(username="test", password="test")
        island = Island.objects.first()
        response = client.get("/i/" + island.name + "/subscribe/subscribe/")
        assert response.status_code == 302 and response.url == "/i/" + island.name + "/"

    def test_adds_subscription(self, client):
        client.login(username="test", password="test")
        user = User.objects.get(username="test")
        island = mommy.make("island.Island")
        client.get(reverse("island:change_subscribe", args=[island.name, "subscribe"]))
        assert user in island.subscribed_by.all()

    def test_removes_subscription(self, client):
        client.login(username="test", password="test")
        user = User.objects.get(username="test")
        island = Island.objects.first()
        client.get(reverse("island:change_subscribe", args=[island.name, "subscribe"]))
        assert user in island.subscribed_by.all()
        client.get(
            reverse("island:change_subscribe", args=[island.name, "unsubscribe"])
        )
        assert user not in island.subscribed_by.all()


class TestIslandDetailView:
    def test_view_exists_at_desired_location(self, client):
        response = client.get("/i/test_island/")
        assert response.status_code == 200

    def test_view_accessible_by_name(self, client):
        response = client.get(reverse("island:detail", args=["test_island"]))
        assert response.status_code == 200

    def test_creation_form_for_invalid_island(self, client):
        response = client.get(reverse("island:detail", args=["island_does_not_exist"]))
        assert response.context["form"]

    # def test_view_is_paginated(self, client):
    #     response = client.get(reverse("island:detail", args=["test_island"]))
    #     assert response.context["is_paginated"]

    # def test_pagination_is_250(self, client):
    #     response = client.get(reverse("island:detail", args=["test_island"]))
    #     assert len(response.context["post_list"]) <= 250

