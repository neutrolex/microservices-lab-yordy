from rest_framework import serializers
from .models import Post
from categories.serializers import CategorySerializer
from authors.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'display_name']


class PostListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    excerpt = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'excerpt', 'author', 
            'category', 'published_at', 'views'
        ]


class PostDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'body', 'author', 
            'category', 'published_at', 'views', 'created_at', 'updated_at'
        ]