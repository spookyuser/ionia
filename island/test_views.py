import pytest
from island.models import Island
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
        response = client.get(
            reverse("island:change_subscribe", args=["test_island", "subscribe"])
        )
        assert response.status_code == 302 and response.url == "/i/test_island/"

    def test_exists_at_desired_location(self, client):
        client.login(username="test", password="test")
        response = client.get("/i/test_island/subscribe/subscribe/")
        assert response.status_code == 302 and response.url == "/i/test_island/"

    def test_adds_subscription(self, client):
        client.login(username="test", password="test")
        client.get(
            reverse("island:change_subscribe", args=["test_island", "subscribe"])
        )
        island = Island.objects.get(name="test_island")
        assert island.created_by in island.subscribed_by.all()

    def test_removes_subscription(self, client):
        client.login(username="test", password="test")
        client.get(
            reverse("island:change_subscribe", args=["test_island", "subscribe"])
        )
        client.get(
            reverse("island:change_subscribe", args=["test_island", "unsubscribe"])
        )
        island = Island.objects.get(name="test_island")
        assert island.created_by not in island.subscribed_by.all()

