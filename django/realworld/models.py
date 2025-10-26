from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.utils import timezone


class User(AbstractUser):
    """Custom User model extending Django's AbstractUser"""
    bio = models.TextField(blank=True, default='')
    image = models.URLField(blank=True, default='')
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'


class Tag(models.Model):
    """Tag model for categorizing articles"""
    name = models.CharField(max_length=50, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tags'
        ordering = ['name']


class Article(models.Model):
    """Article model for blog posts"""
    slug = models.SlugField(unique=True, max_length=255, db_index=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    body = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='articles'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='articles',
        blank=True
    )
    favorited_by = models.ManyToManyField(
        User,
        related_name='favorite_articles',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'articles'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Auto-generate slug from title if not provided"""
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Article.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def favorites_count(self):
        """Return the number of users who favorited this article"""
        return self.favorited_by.count()


class Comment(models.Model):
    """Comment model for article comments"""
    body = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['article', '-created_at']),
        ]

    def __str__(self):
        return f'Comment by {self.author.username} on {self.article.title}'