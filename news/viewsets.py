from rest_framework import viewsets

from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('id')
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('post_id')
    serializer_class = CommentSerializer
