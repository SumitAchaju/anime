from django.urls import path
from .views import AnimeDetailView, AnimeAddCommentsView, AnimeListView, anime_stream

urlpatterns = [
    path("details/<int:pk>/", AnimeDetailView.as_view(), name="anime_detail"),
    path("list/", AnimeListView.as_view(), name="anime_list"),
    path(
        "details/<int:pk>/comments/add/",
        AnimeAddCommentsView.as_view(),
        name="anime_add_comments",
    ),
    path("stream/<int:pk>/ep/<int:ep_num>", anime_stream, name="anime_stream"),
]
