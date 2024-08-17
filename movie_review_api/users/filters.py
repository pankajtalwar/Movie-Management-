# users/filters.py
import django_filters
from .models import Movie, Review,CustomUser

class MovieFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    release_date = django_filters.DateFilter(lookup_expr='exact')

    class Meta:
        model = Movie
        fields = ['title', 'release_date']

class ReviewFilter(django_filters.FilterSet):
    rating = django_filters.NumberFilter(lookup_expr='exact')
    movie = django_filters.ModelChoiceFilter(queryset=Movie.objects.all())
    user = django_filters.ModelChoiceFilter(queryset=CustomUser.objects.all())

    class Meta:
        model = Review
        fields = ['rating', 'movie', 'user']
