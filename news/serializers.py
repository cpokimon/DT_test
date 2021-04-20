from rest_framework import serializers

from .models import Post, Comment


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'link', 'author_name')


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    # post_id = serializers.RelatedField('post_id')

    class Meta:
        model = Comment
        fields = ('post_id', 'author_name', 'content')
