from django.db import models


class AnimeGenreChoices(models.TextChoices):
    ACTION = "Action"
    ADVENTURE = "Adventure"
    COMEDY = "Comedy"
    DRAMA = "Drama"
    ECCHI = "Ecchi"
    FANTASY = "Fantasy"
    HENTAI = "Hentai"
    HORROR = "Horror"
    MAHOU_SHOUJO = "Mahou Shoujo"
    MECHA = "Mecha"
    MUSIC = "Music"
    MYSTERY = "Mystery"
    PSYCHOLOGICAL = "Psychological"
    ROMANCE = "Romance"
    SCI_FI = "Sci-Fi"
    SLICE_OF_LIFE = "Slice of Life"
    SPORTS = "Sports"
    SUPERNATURAL = "Supernatural"
    THRILLER = "Thriller"


class AnimeStatusChoices(models.TextChoices):
    FINISHED = "FINISHED"
    RELEASING = "RELEASING"
    NOT_YET_RELEASED = "NOT_YET_RELEASED"
    CANCELLED = "CANCELLED"
    HIATUS = "HIATUS"


class AnimeFormatChoices(models.TextChoices):
    TV = "TV"
    TV_SHORT = "TV_SHORT"
    MOVIE = "MOVIE"
    SPECIAL = "SPECIAL"
    OVA = "OVA"
    ONA = "ONA"
    MUSIC = "MUSIC"
    MANGA = "MANGA"
    NOVEL = "NOVEL"
    ONE_SHOT = "ONE_SHOT"


class AnimeQualityChoices(models.TextChoices):
    SD = "SD"
    HD = "HD"
    FHD = "FHD"
    UHD = "UHD"
    HDR = "HDR"
    K2 = "2K"
    K4 = "4K"
