from django.test import TestCase, RequestFactory
from django.utils import timezone
from django.urls import reverse
from ..models import Post, Comment
from ..forms import CommentForm


class PostTestCase(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.post_1 = Post.objects.create(
            title='post1_oo',
            link='https://google.com',
            author_name='TestAuthor',
            upvoted=0,
            created=timezone.now,
        )
        self.post_2 = Post.objects.create(
            title='post2_oo',
            link='https://google.com',
            author_name='TestAuthor',
            upvoted=0,
            created=timezone.now,
        )
        self.post_3 = Post.objects.create(
            title='post3_oa',
            link='https://google.com',
            author_name='TestAuthor2',
            upvoted=0,
            created=timezone.now,
        )

    def test_post_list_view_status_code_200(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_post_detail_view_status_code_200(self):
        url = reverse('post_detail', kwargs={'pk': self.post_2.id})
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_post_upvote(self):
        url = reverse('upvote_post', kwargs={'pk': self.post_3.id})
        response = self.client.get(url)
        upvotes = Post.objects.get(id=self.post_3.id).upvoted
        self.assertEqual(302, response.status_code)
        self.assertEqual(1, upvotes)

    def test_post_upvote_post_not_exists_code_302(self):
        url = reverse('upvote_post', kwargs={'pk': 99999})
        response = self.client.get(url)
        self.assertEqual(302, response.status_code)

    def test_post_upvote_post_not_exists_redirect_chain(self):
        url = reverse('upvote_post', kwargs={'pk': 99999})
        response = self.client.get(url, follow=True)
        self.assertEqual([(reverse('home'), 302)], response.redirect_chain)

    def test_post_comment_create_view_code_200(self):
        url = reverse('post_comment', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_post_comment_create_view_creates_comment(self):
        url = reverse('post_comment', kwargs={'pk': self.post_3.id})
        form = CommentForm()
        form.data = {
            'author_name': 'testAuthorName',
            'content': 'testContent',
        }
        response = self.client.post(url, form.data)
        self.assertEqual(302, response.status_code)

        comment = Comment.objects.get(author_name='testAuthorName')
        self.assertEqual(self.post_3.id, comment.post_id)
