from urllib.parse import urlencode

from django.shortcuts import get_object_or_404, reverse, redirect, render
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, ListView
from django_filters.views import FilterView

from anime.filters import AnimeListFilter
from anime.forms import AnimeCommentForm
from anime.models import Anime, AnimeEpisode


class AnimeDetailView(DetailView):
    context_object_name = "anime"
    template_name = "anime/detail.html"

    def get_queryset(self):
        return get_object_or_404(Anime, pk=self.kwargs["pk"])

    def get_object(self, **kwargs):
        return self.get_queryset()


class AnimeListView(FilterView,ListView):
    template_name = "anime/list.html"
    context_object_name = "animes"
    paginate_by = 20
    filterset_class = AnimeListFilter

    # for making at least one query parameter from list
    def dispatch(self, request, *args, **kwargs):
        required_query_params = ['discover', 'keyword', 'genre']
        query = request.GET
        if not any(query.get(param) for param in required_query_params):
            default_params = {
                'genre': 'action'  # or any sensible default
            }
            return redirect(f"{request.path}?{urlencode(default_params)}")
        return super().dispatch(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        size = self.request.GET.get("size")
        if size and size.isdigit():
            try:
                size = int(size)
                if size in [10, 20, 30, 40, 50]:
                    return size
            except ValueError:
                pass
        return super().get_paginate_by(queryset)


class AnimeAddCommentsView(CreateView):
    form_class = AnimeCommentForm

    def get_success_url(self):
        return reverse("anime_detail", kwargs={"pk": self.kwargs["pk"]})

    def get(self, request, *args, **kwargs):
        return redirect(self.get_success_url())


def anime_stream(request, pk, ep_num=1):
    anime = get_object_or_404(Anime, pk=pk)
    episode = AnimeEpisode.objects.filter(anime=anime, episode_number=ep_num).first()
    return render(request, "anime/stream.html", {"anime": anime, "episode": episode})
