from rest_framework import serializers

from .models import Category, Post, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        source='category',
        queryset=Category.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
    )
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        source='tags',
        queryset=Tag.objects.all(),
        many=True,
        required=False,
        write_only=True,
    )

    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'author_username',
            'category',
            'category_id',
            'tags',
            'tag_ids',
            'title',
            'slug',
            'excerpt',
            'content',
            'cover_image',
            'status',
            'is_featured',
            'published_at',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('author', 'created_at', 'updated_at')


class PostListSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'slug',
            'excerpt',
            'cover_image',
            'status',
            'is_featured',
            'published_at',
            'created_at',
            'author_username',
            'category',
            'tags',
        )
