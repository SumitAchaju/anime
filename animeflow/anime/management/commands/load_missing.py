import json

from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404


class Command(BaseCommand):
    help = "load missing anime"

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Path to the JSON file containing missing anime data')


    def handle(self, *args, **kwargs):
        from anime.models import Anime,AnimeEpisode

        with open(kwargs['file'], 'r',encoding='utf-8') as f:
            data = json.load(f)
            for anime in data:
                try:
                    anime_obj = get_object_or_404(Anime, ani_id=anime['ani_id'])
                    episodes = anime.get("streamingEpisodes", [])
                    for episode in episodes:
                        episode_obj, created = AnimeEpisode.objects.update_or_create(
                            anime=anime_obj,
                            episode_number=int(episode['number']),
                            defaults={
                                "title": episode['title'],
                                "jtitle": episode["jname"],
                                "video_url": episode['ep_link'],
                                "episode_number": int(episode['number']),
                            }
                        )
                        if created:
                            self.stdout.write(self.style.SUCCESS(f'Episode "{episode_obj.title}" created.'))
                        else:
                            self.stdout.write(self.style.WARNING(f'Episode "{episode_obj.title}" updated.'))

                    self.stdout.write(self.style.SUCCESS(f'Anime "{anime_obj.title}" updated with episodes.'))

                except Anime.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Anime with ani_id "{anime["ani_id"]}" does not exist.'))

