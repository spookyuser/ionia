# from django.db import models
# import pytest

# from .models import Post
# from island.models import Island
# from user.models import User


# @pytest.fixture(scope="class")
# def post_fixture(django_db_blocker):
#     with django_db_blocker.unblock():
#         user = User.objects.create_user("test", "test@email.com", "test")
#         island = Island.objects.create(user=user, name="test")
#         Post.objects.create(post="test", user=user, Island=island)


# @pytest.mark.usefixtures("post_fixture")
# # @pytest.mark.django_db
# class TestPost:
#     def test_string(self):
#         post = Post.objects.first()
#         assert post.__str__() == post.post
