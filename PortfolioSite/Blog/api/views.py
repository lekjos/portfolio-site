from Blog.api.serializers import PostSerializer
from Blog.models import Post

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
# from rest_framework.permissions import 


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    class Meta:
        model = Post
        fields = "__all__"
