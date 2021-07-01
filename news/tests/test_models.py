from ..models import Post
from django.test import TestCase
from django.utils import timezone


class PostModelTestCase(TestCase):
    def setUp(self) -> None:
        self.post_title = 'TestPost'

        Post.objects.create(
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

