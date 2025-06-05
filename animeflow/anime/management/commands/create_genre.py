from django.core.management.base import BaseCommand
from anime.choices import AnimeGenreChoices
from anime.models import AnimeGenre


class Command(BaseCommand):
    help = "Create Genre from AnimeGenreChoices"

    def handle(self, *args, **kwargs):
        for genre in AnimeGenreChoices:
            genre_obj, created = AnimeGenre.objects.get_or_create(title=genre.label)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Genre "{genre.value}" created.'))
            else:
                self.stdout.write(
                    self.style.WARNING(f'Genre "{genre.value}" already exists.')
                )
