import json
import os
from datetime import datetime

from django.core.management.base import BaseCommand
from anime.models import Anime, AnimeEpisode, AnimeGenre


class Command(BaseCommand):
    help = "Load anime data from JSON file into the database"

    def add_arguments(self, parser):
        parser.add_argument('file_dir', type=str, help='Path to the folder having JSON file containing anime data')

    def handle(self, *args, **kwargs):
        file_dir = kwargs['file_dir'].strip("'").strip('"')

        file_dir = os.path.normpath(file_dir)

        files = [os.path.join(file_dir, file) for file in os.listdir(file_dir) if file.endswith('.json')]

        loaded_anime_count = read_json_file("loaded_anime_info.json")["lastPage"]

        files = files[4:5]

        if not files:
            self.stdout.write(self.style.ERROR('No JSON files found in the specified directory.'))
            return

        for file in files:
            with open(file, 'r',encoding='utf-8') as f:
                data = json.load(f)
                for anime in data:
                    anime_obj, created = Anime.objects.update_or_create(
                        ani_id=anime['id'],
                        defaults=get_defaults(anime)
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Anime "{anime_obj.title}" created.'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Anime "{anime_obj.title}" updated.'))

                     # Handle genres
                    genres = anime.get("genres", [])
                    for genre_name in genres:
                        genre, _ = AnimeGenre.objects.get_or_create(title=genre_name)
                        anime_obj.genres.add(genre)

                    # handle episodes
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

            self.stdout.write(self.style.SUCCESS(f'Successfully loaded data from {file}.'))
            loaded_anime_count += 1
            write_json_file("loaded_anime_info.json", {"lastPage": loaded_anime_count})


def get_defaults(anime):
    return {
        "ani_id": anime['id'],
        'title': anime['title'].get('english') or anime['title'].get('romaji'),
        'jtitle': anime['title'].get('romaji'),
        "native": anime['title'].get('native'),
        'description': anime['description'],
        'release_date': anime['startDate'],
        'end_date': anime.get('endDate'),
        'thumbnail': anime['coverImage'],
        'banner_image': anime.get('bannerImage'),
        'average_score': anime.get('averageScore'),
        'mean_score': anime.get('meanScore'),
        'trending': anime.get('trending'),
        'popularity': anime.get('popularity'),
        'favourites': anime.get('favourites'),
        'status': anime['status'],
        'format': anime['format'],
        'season': anime['season'],
        'season_year': anime['seasonYear'],
        'episodes_count': anime['episodes'],
        'duration': anime['duration'],
        'chapters': anime.get('chapters'),
        'volumes': anime.get('volumes'),
        'country_of_origin': anime.get('countryOfOrigin'),
        'source': anime.get('source'),
        'ani_update_at': datetime.fromtimestamp(anime.get('updatedAt')),
        'studio': anime.get('studios'),
        'synonyms': anime.get('synonyms'),
    }

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def write_json_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)