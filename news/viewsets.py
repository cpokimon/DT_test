from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('id')
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['title']
    search_fields = ['title', 'author_name']
    ordering_fields = ['title', 'author_name']


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('post_id', 'id')
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['author_name']
    search_fields = ['author_name', 'post__title']
    ordering_fields = ['id', 'created', 'author_name', 'post_id']

