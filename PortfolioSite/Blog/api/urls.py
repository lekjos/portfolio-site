from django.urls import path
from django.urls import include

from rest_framework.authtoken import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
# from Blog.api.views import PostList, PostDetail
from Blog.api.views import PostViewSet

router = DefaultRouter()
router.register('posts',PostViewSet)


urlpatterns = [
    path("auth/", include('rest_framework.urls')),
    path("token-auth/", views.obtain_auth_token),
    path("", include(router.urls))
]

# not needed with routers
# urlpatterns = format_suffix_patterns(urlpatterns, allowed='json')