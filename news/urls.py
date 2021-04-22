from django.urls import include, path
from .views import upvoute_post_api, PostListView, \
                   PostDetailView, post_comment_create_view, \
                   upvote_post_view
from .routers import router


urlpatterns = [
    path('api/', include(router.urls)),
    path('', PostListView.as_view(), name='home'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/comment', post_comment_create_view, name='post_comment'),
    path('posts/<int:pk>/upvote', upvote_post_view, name='upvote_post'),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('api/posts/<int:pk>/upvote', upvoute_post_api, name='post_upvote'),
]
