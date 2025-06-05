from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import JSONField

from .choices import (
    AnimeGenreChoices,
    AnimeStatusChoices,
    AnimeFormatChoices,
)


class AnimeGenre(models.Model):
    title = models.CharField(max_length=255, choices=AnimeGenreChoices.choices)

    def __str__(self):
        return self.title


class AnimeRating(models.Model):
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    anime = models.ForeignKey("Anime", on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.anime.title} - {self.rating}"


class AnimeComments(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    anime = models.ForeignKey(
        "Anime", on_delete=models.CASCADE, related_name="comments"
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.anime.title} - {self.comment[:20]}"


class AnimeEpisode(models.Model):
    anime = models.ForeignKey("Anime", on_delete=models.CASCADE, related_name="episodes")
    title = models.CharField(max_length=255)
    jtitle = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    duration = models.SmallIntegerField(null=True, blank=True)
    thumbnail = JSONField(default=dict)
    video_url = models.URLField()
    episode_number = models.IntegerField()

    def __str__(self):
        return f"{self.anime.title} - Episode {self.episode_number}"


class Anime(models.Model):
    ani_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    jtitle = models.CharField(max_length=255, null=True, blank=True)
    native = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    release_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    thumbnail = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    duration = models.SmallIntegerField(null=True, blank=True)
    views = models.BigIntegerField(default=0)
    studio = models.CharField(max_length=255, default="Mappa",null=True, blank=True)
    format = models.CharField(
        max_length=255,
        choices=AnimeFormatChoices.choices,
        default=AnimeFormatChoices.TV,
    )
    status = models.CharField(
        max_length=255,
        choices=AnimeStatusChoices.choices,
        default=AnimeStatusChoices.FINISHED,
    )
    genres = models.ManyToManyField(AnimeGenre, related_name="animes")
    synonyms = models.JSONField(default=list)
    average_score = models.IntegerField(default=0,null=True,blank=True)
    mean_score = models.IntegerField(default=0,null=True,blank=True)
    popularity = models.IntegerField(default=0,null=True,blank=True)
    favourites = models.IntegerField(default=0,null=True,blank=True)
    trending = models.IntegerField(default=0,null=True,blank=True)
    banner_image = models.URLField(null=True, blank=True)
    source = models.CharField(max_length=255,null=True, blank=True)
    volumes = models.IntegerField(null=True,blank=True)
    chapters = models.IntegerField(null=True,blank=True)
    episodes_count = models.IntegerField(null=True,blank=True)
    season = models.CharField(max_length=20,null=True,blank=True)
    season_year = models.IntegerField(null=True,blank=True)
    country_of_origin = models.CharField(max_length=25,null=True,blank=True)
    ani_update_at = models.DateTimeField(null=True, blank=True)


    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return sum(rating.rating for rating in ratings) / ratings.count()
        return 0.0

    def __str__(self):
        return self.title
