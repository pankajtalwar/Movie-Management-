# users/management/commands/recommendations.py
from django.core.management.base import BaseCommand
from users.models import Review, Movie
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

class Command(BaseCommand):
    help = 'Generate movie recommendations based on user reviews'

    def handle(self, *args, **kwargs):
    # Fetch all reviews and movies
        reviews = Review.objects.all().select_related('movie', 'user')
        movies = Movie.objects.all()

        if not reviews.exists():
            self.stdout.write("No reviews found.")
            return

        if not movies.exists():
            self.stdout.write("No movies found.")
            return

        # Create a DataFrame from the reviews
        review_data = pd.DataFrame(list(reviews.values('user_id', 'movie_id', 'rating', 'comment')))

        # Create a pivot table with users as rows and movies as columns
        pivot_table = review_data.pivot_table(index='user_id', columns='movie_id', values='rating')

        # Fill missing values with 0 (for simplicity)
        pivot_table = pivot_table.fillna(0)

        if pivot_table.empty:
            self.stdout.write("Pivot table is empty. No data available for recommendations.")
            return

        self.stdout.write(f"Available user IDs: {pivot_table.index.tolist()}")

        # Example: Get recommendations for a user
        user_id = 2  # Replace with actual user ID

        if user_id not in pivot_table.index:
            self.stdout.write(f"User ID {user_id} not found in the pivot table.")
            return

        user_ratings = pivot_table.loc[user_id]

        # Calculate cosine similarity between movies
        movie_similarity = cosine_similarity(pivot_table.T)

        # Create a DataFrame for movie similarity
        movie_similarity_df = pd.DataFrame(movie_similarity, index=pivot_table.columns, columns=pivot_table.columns)

        if movie_similarity_df.empty:
            self.stdout.write("Movie similarity DataFrame is empty.")
            return

        # Predict ratings for unseen movies
        predictions = movie_similarity_df.dot(user_ratings) / movie_similarity_df.sum(axis=1)

        # Sort movies by predicted rating
        recommendations = predictions.sort_values(ascending=False).head(10)

        # Print recommendations
        self.stdout.write("Recommended Movies:")
        for movie_id in recommendations.index:
            try:
                movie = Movie.objects.get(id=movie_id)
                self.stdout.write(f"Recommended Movie: {movie.title}, Predicted Rating: {recommendations[movie_id]}")
            except Movie.DoesNotExist:
                self.stdout.write(f"Movie with ID {movie_id} does not exist.")
