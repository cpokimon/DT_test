from django.test import TestCase
from django.utils import timezone
from ..models import Post
from ..tasks import reset_upvoutes


class TasksTestCase(TestCase):
    def setUp(self) -> None:
        self.post_1 = Post.objects.create(
            title="testTitle",
            link='https://google.com',
            author_name='TestAuthor1',
            upvoted=100,
            created=timezone.now,
        )
        self.post_2 = Post.objects.create(
            title="testTitle",
            link='https://google.com',
            author_name='TestAuthor2',
            upvoted=50,
            created=timezone.now,
        )

    def test_reset_upvotes(self):
        reset_upvoutes()
        self.post_1.refresh_from_db()
        self.post_2.refresh_from_db()

        self.assertEqual(0, self.post_1.upvoted)
        self.assertEqual(0, self.post_2.upvoted)
