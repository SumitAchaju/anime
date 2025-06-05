from django.contrib import admin

from anime.models import Anime, AnimeGenre, AnimeRating, AnimeComments, AnimeEpisode


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "native",
        "description",
        "release_date",
        "average_rating",
        "created_at",
    )
    search_fields = ("title", "native", "description",'ani_id')
    list_filter = ("release_date", "genres__title")
    ordering = ("-created_at",)
    list_per_page = 20

@admin.register(AnimeEpisode)
class AnimeEpisodeAdmin(admin.ModelAdmin):
    list_display = ("anime", "title", "episode_number", "release_date")
    search_fields = ("anime__title", "title")
    ordering = ("episode_number",)
    list_per_page = 20

@admin.register(AnimeGenre)
class AnimeGenreAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)
    ordering = ("title",)
    list_per_page = 20


@admin.register(AnimeRating)
class AnimeRatingAdmin(admin.ModelAdmin):
    list_display = ("rating", "anime", "user")
    search_fields = ("anime__title", "user__username")
    ordering = ("-rating",)
    list_per_page = 20


@admin.register(AnimeComments)
class AnimeCommentsAdmin(admin.ModelAdmin):
    list_display = ("user", "anime", "comment", "created_at")
    search_fields = ("anime__title", "user__username")
    ordering = ("-created_at",)
    list_per_page = 20
