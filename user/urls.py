"""All urls specific to User"""

from django.urls import path

from . import views

app_name = "user"
urlpatterns = [
    path("users/<str:pk>", views.DetailView.as_view(), name="detail"),
    path("users/<str:username>/follow/<str:action>/", views.change_follow, name="change_follow"),
    path("users/register/", views.RegisterView.as_view(), name="register"),
    path("users/email_change/", views.ChangeEmail.as_view(), name="email_change"),
    path(
        "users/email_change/done/",
        views.ChangeEmailDone.as_view(),
        name="email_change_done",
    ),
]
