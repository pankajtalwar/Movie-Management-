from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from .models import Movie
from .serializers import MovieSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import MovieFilter,ReviewFilter
from rest_framework.pagination import PageNumberPagination

##Adding Descriptions
from drf_yasg.utils import swagger_auto_schema


from .models import Review
from .serializers import ReviewSerializer
from users import filters


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("Logout view accessed")
        print(f"Request user: {request.user}")
        
        if not request.user or not request.user.auth_token:
            print("No user or token found")
            return Response({"error": "Invalid token or user not logged in"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            request.user.auth_token.delete()
            print("Token deleted")
            return Response({"message": "Logged out successfully!"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            print("Token does not exist")
            return Response({"error": "Invalid token or user not logged in"}, status=status.HTTP_400_BAD_REQUEST)


###above is working

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    
# Retrieve, Update, and Delete Reviews
class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied("You do not have permission to access this review.")
        return obj
    
class MovieListCreateView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MovieRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return super().get_object()
    
class MoviePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = MoviePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MovieFilter
    ordering_fields = '__all__'

    @swagger_auto_schema(
        operation_description="Retrieve a list of movies",
        responses={200: MovieSerializer(many=True)},
        tags=['Movies']  # Optional: Add a tag to group endpoints
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ReviewListView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter

class MoviePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ReviewPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


