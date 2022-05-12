from Blog.models import Post, Tag
from Blog.api.serializers import PostSerializer, TagSerializer
from Blog.api.permissions import AuthorModifyOrReadOnly, IsObjectAdmin

from rest_framework import viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
# from rest_framework.permissions import 


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permissions_classes = [AuthorModifyOrReadOnly | IsObjectAdmin]
    
    class Meta:
        model = Post
        fields = "__all__"

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    @action(methods=["get"], detail=True, name="Posts with Tag")
    def posts(self,request,pk=None):
        tag = self.get_object()
        post_serializer = PostSerializer(
            tag.posts, many=True, context={"request":request}
        )
        return Response(post_serializer.data)