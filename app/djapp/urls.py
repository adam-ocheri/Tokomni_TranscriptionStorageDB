from django.urls import path
from . import views
from .views import ConversationItemView, CallPartView
urlpatterns = [
    path("", views.home, name="home"),
    path("items/", views.items, name="db-items"),
    path("search/", views.search, name="search"),
    path("api/conv_items", ConversationItemView.as_view(), name="list__conv_items"),
    path("api/conv_items/<int:pk>/", ConversationItemView.as_view(), name="detail__conv_items"),
    path("api/call_parts", CallPartView.as_view(), name="endpoint__call_parts")
]