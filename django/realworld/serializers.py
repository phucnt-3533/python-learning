from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Article, Comment, Tag


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            # Try to authenticate with email as username
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

            if not user:
                raise serializers.ValidationError('Invalid credentials')

            data['user'] = user
            return data
        else:
            raise serializers.ValidationError('Must include email and password')


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profiles"""
    following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'bio', 'image', 'following']

    def get_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.following.filter(id=obj.id).exists()
        return False


class UserSerializer(serializers.ModelSerializer):
    """Serializer for authenticated user with token"""
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'username', 'bio', 'image', 'token']

    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh.access_token)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags"""
    class Meta:
        model = Tag
        fields = ['name']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments"""
    author = ProfileSerializer(read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'body', 'author', 'createdAt', 'updatedAt']
        read_only_fields = ['id', 'author', 'createdAt', 'updatedAt']


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for articles"""
    author = ProfileSerializer(read_only=True)
    tagList = serializers.SerializerMethodField()
    favoritesCount = serializers.SerializerMethodField()
    favorited = serializers.SerializerMethodField()
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)
    description = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Article
        fields = [
            'slug', 'title', 'description', 'body', 'tagList',
            'createdAt', 'updatedAt', 'favorited', 'favoritesCount', 'author'
        ]
        read_only_fields = ['slug', 'author', 'createdAt', 'updatedAt']

    def get_tagList(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def get_favoritesCount(self, obj):
        return obj.favorited_by.count()

    def get_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorited_by.filter(id=request.user.id).exists()
        return False

    def create(self, validated_data):
        # Extract tags from request data if present
        request = self.context.get('request')
        tag_list = []
        if request and hasattr(request, 'data'):
            tag_list = request.data.get('article', {}).get('tagList', [])

        # Create article
        article = Article.objects.create(**validated_data)

        # Add tags
        if tag_list:
            for tag_name in tag_list:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                article.tags.add(tag)

        return article

    def update(self, instance, validated_data):
        # Update article fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Handle tags if present
        request = self.context.get('request')
        if request and hasattr(request, 'data'):
            tag_list = request.data.get('article', {}).get('tagList')
            if tag_list is not None:
                instance.tags.clear()
                for tag_name in tag_list:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    instance.tags.add(tag)

        instance.save()
        return instance


class ArticleCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating articles"""
    tagList = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True
    )

    class Meta:
        model = Article
        fields = ['title', 'description', 'body', 'tagList']

    def create(self, validated_data):
        tag_list = validated_data.pop('tagList', [])
        article = Article.objects.create(**validated_data)

        # Add tags
        for tag_name in tag_list:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            article.tags.add(tag)

        return article
