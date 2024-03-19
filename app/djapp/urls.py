from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("items/", views.items, name="db-items"),
    path("main/", views.main, name="main")
]