from anime.models import AnimeGenre


def anime_genre(request):
    return {"anime_genre": AnimeGenre.objects.all()}
