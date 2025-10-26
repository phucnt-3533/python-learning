from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserRegistrationView,
    UserLoginView,
    CurrentUserView,
    ProfileView,
    FollowUserView,
    ArticleViewSet,
    CommentViewSet,
    TagListView,
)

# Create router for viewsets
router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')

# URL patterns
urlpatterns = [
    # Authentication endpoints
    path('users/', UserRegistrationView.as_view(), name='user-register'),
    path('users/login/', UserLoginView.as_view(), name='user-login'),
    path('user/', CurrentUserView.as_view(), name='current-user'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # Profile endpoints
    path('profiles/<str:username>/', ProfileView.as_view(), name='profile'),
    path('profiles/<str:username>/follow/', FollowUserView.as_view(), name='profile-follow'),

    # Tags endpoint
    path('tags/', TagListView.as_view(), name='tags'),

    # Article comments (nested routes)
    path('articles/<slug:article_slug>/comments/', CommentViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='article-comments'),
    path('articles/<slug:article_slug>/comments/<int:pk>/', CommentViewSet.as_view({
        'delete': 'destroy'
    }), name='article-comment-detail'),

    # Article favorite endpoints
    path('articles/<slug:slug>/favorite/', ArticleViewSet.as_view({
        'post': 'favorite',
        'delete': 'unfavorite'
    }), name='article-favorite'),

    # Router URLs (includes article CRUD and feed)
    path('', include(router.urls)),
]
