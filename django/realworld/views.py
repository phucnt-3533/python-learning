from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .models import User, Article, Comment, Tag
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    ProfileSerializer,
    ArticleSerializer,
    CommentSerializer,
    TagSerializer,
)
from .permissions import IsAuthorOrReadOnly, IsCommentAuthorOrReadOnly
from .filters import ArticleFilter


class UserRegistrationView(APIView):
    """User registration endpoint"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data.get('user', {}))
        if serializer.is_valid():
            user = serializer.save()
            user_serializer = UserSerializer(user, context={'request': request})
            return Response({'user': user_serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """User login endpoint"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data.get('user', {}))
        if serializer.is_valid():
            user = serializer.validated_data['user']
            user_serializer = UserSerializer(user, context={'request': request})
            return Response({'user': user_serializer.data}, status=status.HTTP_200_OK)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
    """Get and update current user"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response({'user': serializer.data})

    def put(self, request):
        serializer = UserSerializer(
            request.user,
            data=request.data.get('user', {}),
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({'user': serializer.data})
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    """User profile view"""
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, username):
        profile = get_object_or_404(User, username=username)
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response({'profile': serializer.data})


class FollowUserView(APIView):
    """Follow/unfollow a user"""
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        profile = get_object_or_404(User, username=username)
        request.user.following.add(profile)
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response({'profile': serializer.data})

    def delete(self, request, username):
        profile = get_object_or_404(User, username=username)
        request.user.following.remove(profile)
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response({'profile': serializer.data})


class ArticleViewSet(viewsets.ModelViewSet):
    """ViewSet for articles"""
    queryset = Article.objects.select_related('author').prefetch_related('tags', 'favorited_by')
    serializer_class = ArticleSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ArticleFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data.get('article', {}),
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'article': serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'article': serializer.data})

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'articles': serializer.data, 'articlesCount': queryset.count()})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data.get('article', {}),
            partial=partial,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'article': serializer.data})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def feed(self, request):
        """Get articles from followed users"""
        following_users = request.user.following.all()
        queryset = Article.objects.filter(author__in=following_users).select_related('author').prefetch_related('tags', 'favorited_by')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'articles': serializer.data, 'articlesCount': queryset.count()})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def favorite(self, request, slug=None):
        """Favorite an article"""
        article = self.get_object()
        request.user.favorite_articles.add(article)
        serializer = self.get_serializer(article)
        return Response({'article': serializer.data})

    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def unfavorite(self, request, slug=None):
        """Unfavorite an article"""
        article = self.get_object()
        request.user.favorite_articles.remove(article)
        serializer = self.get_serializer(article)
        return Response({'article': serializer.data})


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for comments on articles"""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCommentAuthorOrReadOnly]

    def get_queryset(self):
        article_slug = self.kwargs.get('article_slug')
        return Comment.objects.filter(article__slug=article_slug).select_related('author', 'article')

    def perform_create(self, serializer):
        article_slug = self.kwargs.get('article_slug')
        article = get_object_or_404(Article, slug=article_slug)
        serializer.save(author=self.request.user, article=article)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data.get('comment', {}))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'comment': serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'comments': serializer.data})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagListView(generics.ListAPIView):
    """List all tags"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        tags = [tag['name'] for tag in serializer.data]
        return Response({'tags': tags})
