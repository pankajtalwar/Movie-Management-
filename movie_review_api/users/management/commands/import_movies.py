from django.core.management.base import BaseCommand
from users.models import Movie, Genre, CustomUser
from users.utils import fetch_all_movies

class Command(BaseCommand):
    help = 'Fetches and stores movies from TMDb API'

    def handle(self, *args, **options):
        # Fetch movies with a limit of 20
        all_movies = fetch_all_movies(max_count=20)
        
        # Get the first CustomUser or handle if no users exist
        user = CustomUser.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR('No CustomUser found. Please create at least one user.'))
            return

        for movie_data in all_movies:
            # Extract genre IDs and get corresponding Genre objects
            genre_ids = movie_data.get('genre_ids', [])
            genres = []
            for genre_id in genre_ids:
                try:
                    genre_obj = Genre.objects.get(tmdb_id=genre_id)
                    genres.append(genre_obj)
                except Genre.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Genre with TMDb ID {genre_id} not found"))

            # Create or update movie
            movie, created = Movie.objects.update_or_create(
                tmdb_id=movie_data['id'],
                defaults={
                    'title': movie_data['title'],
                    'description': movie_data.get('overview', ''),
                    'release_date': movie_data.get('release_date', None),
                    'poster_url': f"https://image.tmdb.org/t/p/w500{movie_data.get('poster_path', '')}",
                    'user': user  # Add the user field here if it's required
                }
            )

            # Assign genres to the movie
            movie.genres.set(genres)
            movie.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully saved {len(all_movies)} movies'))
