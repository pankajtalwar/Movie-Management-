from django.contrib import admin
from .models import CustomUser,Review,Genre,Movie

admin.site.register(CustomUser)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'get_genres', 'user')
    list_filter = ('genres',)
    search_fields = ('title',)

    # Method to display genres in the admin list
    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = 'Genres'

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'tmdb_id')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'movie', 'rating', 'comment')
    list_filter = ('user', 'movie', 'rating')
    search_fields = ('comment', 'movie__title')