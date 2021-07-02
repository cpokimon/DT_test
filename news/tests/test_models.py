from ..models import Post
from django.test import TestCase
from django.utils import timezone


class PostModelTestCase(TestCase):
    def setUp(self) -> None:
        self.post_title = 'TestPost'

        self.post = Post.objects.create(
            title=self.post_title,
            link='https://google.com',
            author_name='TestAuthor',
            upvoted=0,
            created=timezone.now,
        )

    def test_post_upvote(self):
        post_first_request = Post.objects.get(title=self.post_title)
        post_second_request = Post.objects.get(title=self.post_title)

        post_first_request.upvote()
        post_first_request.save()
        post_first_request.refresh_from_db()
        self.assertEqual(1, post_first_request.upvoted)

        post_second_request.upvote()
        post_second_request.save()
        post_second_request.refresh_from_db()
        self.assertEqual(2, post_second_request.upvoted)

    def test_str(self):
        self.assertEqual(
            f'ID:{self.post.id}, TITLE:{self.post.title[:10]}',
            self.post.__str__(),
        )

