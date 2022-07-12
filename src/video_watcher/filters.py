from django_filters import rest_framework as filters

from src.video_watcher.models import Serial


class CharFilterMix(filters.BaseInFilter, filters.CharFilter):
    pass


class SerialFilter(filters.FilterSet):
    date = filters.DateFilter()
    genres = CharFilterMix(field_name='genres__name', lookup_expr='in')
    studio = CharFilterMix(field_name='studio__name', lookup_expr='in')

    class Meta:
        model = Serial
        fields = ['date', 'studio', 'genres']
