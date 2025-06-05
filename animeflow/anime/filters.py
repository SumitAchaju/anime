import django_filters

from anime.models import Anime
from django.db.models import Q


class AnimeListFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(field_name="genres__title", lookup_expr="iexact")
    keyword = django_filters.CharFilter(method="filter_by_title_or_synonyms")
    discover = django_filters.CharFilter(method="filter_by_highlights")
    order_by = django_filters.OrderingFilter(
        fields=(
            ('title', 'title'),
            ('release_date', 'release_date'),
            ('popularity', 'popularity'),
        ),
        field_labels={
            'title': 'Title',
            'release_date': 'Release Date',
            'popularity': 'Popularity',
        })

    class Meta:
        model = Anime
        fields = []

    @staticmethod
    def filter_by_title_or_synonyms( queryset, _, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(synonyms__icontains=value)
        )

    @staticmethod
    def filter_by_highlights( queryset, _, value):
        return queryset
