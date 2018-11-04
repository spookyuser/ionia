"""All urls specific to Island"""

from django.urls import path

from . import views

app_name = "island"
urlpatterns = [
    path("i/<str:pk>/", views.DetailView.as_view(), name="detail"),
    path("i/<str:pk>/sort/<str:sort>/", views.DetailView.as_view(), name="detail_sort"),
    path("island/create/", views.CreateView.as_view(), name="create"),
    path("islands/", views.ListView.as_view(), name="list"),
    path("i/<str:island>/subscribe/<str:action>/", views.change_subscribe, name="change_subscribe"),
]
