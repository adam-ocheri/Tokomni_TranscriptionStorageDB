from django.urls import path
from . import views
from .views import ConversationItemView
urlpatterns = [
    path("", views.home, name="home"),
    path("items/", views.items, name="db-items"),
    path("search/", views.search, name="search"),
    path("api/", ConversationItemView.as_view(), name="endpoint")
]