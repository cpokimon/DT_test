from django.urls import include, path
from .views import upvoute_post
from .routers import router


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('posts/<int:id>/upvout', upvoute_post, name='post_upvout'),
]
