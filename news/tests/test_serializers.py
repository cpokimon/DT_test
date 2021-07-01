from django.test import TestCase
from django.utils import timezone
from ..models import Post, Comment
from ..serializers import PostSerializer, CommentSerializer


class PostSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.post_1 = Post.objects.create(
            title='post2',
            link='https://google.com',
            author_name='TestAuthor',
            upvoted=0,
            created=timezone.now,
        )
        self.post_2 = Post.objects.create(
            title='post1',
            link='https://google.com',
            author_name='TestAuthor',
            upvoted=0,
            created=timezone.now,
        )

    def test_ok(self):
        data = PostSerializer([self.post_1, self.post_2], many=True).data
        expected_data = [
            {
                'id': self.post_1.id,
                'title': self.post_1.title,
                'link': self.post_1.link,
                'author_name': self.post_1.author_name,
            },
            {
                'id': self.post_2.id,
                'title': self.post_2.title,
                'link': self.post_2.link,
                'author_name': self.post_2.author_name,
            },
        ]
        self.assertEqual(expected_data, data)


class CommentSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.post = Post.objects.create(
            title='post2',
            link='https://google.com',
            author_name='TestAuthor',
            upvoted=0,
            created=timezone.now,
        )
        self.comment_1 = Comment.objects.create(
            post=self.post,
            author_name='TestAuthor',
            content='Test comment content 1',
            created=timezone.now,
        )
        self.comment_2 = Comment.objects.create(
            post=self.post,
            author_name='TestAuthor',
            content='Test comment content 2',
            created=timezone.now,
        )

    def test_ok(self):
        data = CommentSerializer([self.comment_1, self.comment_2], many=True).data
        expected_data = [
            {
                'id': self.comment_1.id,
                'post_id': self.comment_1.post_id,
                'author_name': self.comment_1.author_name,
                'content': self.comment_1.content,
            },
            {
                'id': self.comment_2.id,
                'post_id': self.comment_2.post_id,
                'author_name': self.comment_2.author_name,
                'content': self.comment_2.content,
            },
        ]
        self.assertEqual(expected_data, data)
