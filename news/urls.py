from django.urls import include, path
from .views import upvoute_post, PostListView, PostDetailView
from .routers import router


urlpatterns = [
    path('api/', include(router.urls)),
    path('', PostListView.as_view()),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('api/posts/<int:id>/upvote', upvoute_post, name='post_upvote'),
]
