from django.urls import path
from django.urls import include

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
# from Blog.api.views import PostList, PostDetail
from Blog.api.views import PostViewSet

router = DefaultRouter()
router.register('posts',PostViewSet)


urlpatterns = [
    path("", include(router.urls))
]

# urlpatterns = format_suffix_patterns(urlpatterns, allowed='json')