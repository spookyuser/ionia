"""All urls specific to Post"""

from django.urls import path

from . import views

app_name = "post"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("list/<str:list>/<str:sort>/", views.IndexView.as_view(), name="index_list"),
    path("post/new/", views.save_post, name="new"),
    path("post/<int:pk>/like/<str:action>", views.change_like, name="change_like"),
    path("i/<str:island>/post/<int:pk>", views.DetailView.as_view(), name="detail"),
]
