# from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

# You can customize the user model if needed, or use the built-in User model
class CustomUser(AbstractUser):
    pass

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE,null=True)
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"{self.movie.title} - {self.user.username} - {self.rating}"
    

class Genre(models.Model):
    name = models.CharField(max_length=255,default='Unknown')
    tmdb_id = models.IntegerField(unique=True,default=0)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    genres = models.ManyToManyField(Genre)
    poster_url = models.URLField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tmdb_id = models.IntegerField(unique=True)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='movies')


    def __str__(self):
        return self.title
    
