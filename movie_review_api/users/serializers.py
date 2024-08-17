from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Review,Movie


User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user
    

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    return user
                else:
                    raise serializers.ValidationError("User is deactivated.")
            else:
                raise serializers.ValidationError("Invalid credentials.")
        else:
            raise serializers.ValidationError("Must include both username and password.")


###above is working

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'movie_title', 'rating', 'content']
        read_only_fields = ['user']

class MovieSerializer(serializers.ModelSerializer):
    genres = serializers.StringRelatedField(many=True) 
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'release_date', 'genres', 'poster_url']
        read_only_fields = ['user']

class ReviewSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = ['id', 'user', 'movie', 'rating', 'comment']
