from django.test import TestCase
from django.utils import timezone
from ..forms import CommentForm
from ..models import Post, Comment


class CommentFormTestCase(TestCase):
    def setUp(self) -> None:
        self.post = Post.objects.create(
            title='post1_oo',
            link='https://google.com',
            author_name='TestAuthor',
            upvoted=0,
            created=timezone.now,
        )
        form_data = {
            'author_name': 'TestAuthorNameUnique228',
            'content': 'Test content',
            'post_id': self.post.id
        }
        self.form = CommentForm(data=form_data)

    def test_comment_form_is_valid(self):
        self.assertTrue(self.form.is_valid())

    def test_comment_form_save(self):
        if self.form.is_valid():
            self.form.cleaned_data['post_id'] = self.post.id
            self.form.save()
        comment = Comment.objects.get(author_name='TestAuthorNameUnique228')
        self.assertEqual(self.post.id, comment.post_id)
        self.assertEqual('Test content', comment.content)

    def test_comment_form_clean_created_returns_none(self):
        self.assertEqual(None, self.form.clean_created())

    def test_comment_form_clean_post_id_returns_post_id(self):
        self.form.is_valid()
        self.form.cleaned_data['post_id'] = self.post.id
        self.assertEqual(self.post.id, self.form.clean_post_id())
