from Auth.models import User
from rest_framework import serializers
from Blog.models import Post, Tag, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['__all__']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        slug_field="value",
        many=True,
        queryset=Tag.objects.all()
        )

    class Meta:
        model = Post
        fields = '__all__'
        readonly = ["modified_at", "created_at"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'