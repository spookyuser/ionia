import pytest
from post.models import Post
from post.forms import PostForm
from django.urls import reverse

"""From https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing#Views"""

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def disable_axes(settings):
    if "axes" in settings.INSTALLED_APPS:
        settings.AUTHENTICATION_BACKENDS.remove("axes.backends.AxesModelBackend")
        settings.INSTALLED_APPS.remove("axes")

class TestPostListView:
    def test_view_exists_at_desired_location(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_view_accessible_by_name(self, client):
        response = client.get(reverse("post:index"))
        assert response.status_code == 200
    
    def test_lists_all_posts(self, client):
        response = client.get((reverse("post:index") + "?page=2"))
        assert len(response.context["post_list"]) == 10
    
class TestPostDetailView:
    def test_view_exists_at_desired_location(self, client):
        post = Post.objects.first()
        response = client.get("/i/" + post.island.name + str(post.id) + "/")
        assert response.status_code == 200

    def test_view_accessible_by_name(self, client):
        post = Post.objects.first()
        response = client.get(reverse("post:detail", args=[post.island, post.id]))
        assert response.status_code == 200
    
    def test_post_detail_text_matches_post(self, client):
        post = Post.objects.first()
        response = client.get(reverse("post:detail", args=[post.island, post.id]))
        assert response.context["post"].post == post.post

class TestSavePost:
    def test_exists_at_desired_location(self, client):
        post = Post.objects.first()
        response = client.get("/post/new/")
        assert response.status_code == 302

    def test_accessible_by_name(self, client):
        response = client.get(reverse("post:new"))
        assert response.status_code == 302

    def test_save_post_saves_post(self, client):
        client.login(username="test", password="test")
        data = {"post": "This is a post", "island" : "test"}
        client.post(reverse("post:new"), data=data)
        client.logout()
        response = client.get(reverse("post:index"))
        assert len([post for post in response.context["post_list"] if "This is a post" in post.post]) == 1
        