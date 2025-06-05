from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "extract anime into json file that doesnot have episodes"

    def handle(self, *args, **kwargs):
        from anime.models import Anime
        from django.core.serializers.json import DjangoJSONEncoder
        import json

        animes = Anime.objects.filter(episodes__isnull=True)

        data = []
        for anime in animes:
            data.append({
                "id": anime.id,
                "title": anime.title,
                "jtitle": anime.jtitle,
                "ani_id": anime.ani_id,
                "format": anime.format,
                "status": anime.status,
                "startDate": anime.release_date.strftime("%Y-%m-%d"),
                "endDate": anime.end_date.strftime("%Y-%m-%d") if anime.end_date else None,
                "genres": [genre.title for genre in anime.genres.all()],
                "episodes": anime.episodes_count,
            })

        with open("missing_anime.json", "w", encoding="utf-8") as f:
            json.dump(data, f, cls=DjangoJSONEncoder, ensure_ascii=False, indent=4)