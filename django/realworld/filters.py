from django_filters import rest_framework as filters
from .models import Article


class ArticleFilter(filters.FilterSet):
    """Filter for articles by tag, author, and favorited"""
    tag = filters.CharFilter(field_name='tags__name', lookup_expr='iexact')
    author = filters.CharFilter(field_name='author__username', lookup_expr='iexact')
    favorited = filters.CharFilter(method='filter_favorited')

    class Meta:
        model = Article
        fields = ['tag', 'author', 'favorited']

    def filter_favorited(self, queryset, name, value):
        """Filter articles favorited by a specific username"""
        return queryset.filter(favorited_by__username=value)
