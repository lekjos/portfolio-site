from Blog.api.permissions import AuthorModifyOrReadOnly, IsObjectAdmin

from rest_framework import viewsets
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
