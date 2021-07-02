from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from ..models import Post, Comment
from ..serializers import PostSerializer, CommentSerializer
from ..views import upvoute_post_api
from django.utils import timezone


class PostsApiTestCase(APITestCase):
    def setUp(self) -> None:
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

    def test_get(self):
        url = reverse('post-list')
        response = self.client.get(url)

        serializer_data = PostSerializer([self.post_1, self.post_2, self.post_3], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_filter(self):
        url = reverse('post-list')
        response = self.client.get(url, data={'title': 'post1_oo'})

        serializer_data = PostSerializer(self.post_1).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.data['results']))
        self.assertEqual(serializer_data, response.data['results'][0])

    def test_get_search(self):
        url = reverse('post-list')
        responce = self.client.get(url, data={'search': 'oo'})

        serializer_data = PostSerializer([self.post_1, self.post_2], many=True).data

        self.assertEqual(status.HTTP_200_OK, responce.status_code)
        self.assertEqual(serializer_data, responce.data['results'])

    def test_get_ordering(self):
        url = reverse('post-list')
        responce = self.client.get(url, data={'ordering': '-author_name'})

        serializer_data = PostSerializer([self.post_3, self.post_1, self.post_2], many=True).data

        self.assertEqual(status.HTTP_200_OK, responce.status_code)
        self.assertEqual(serializer_data, responce.data['results'])

    def test_upvote_post(self):
        url = reverse('post_upvote', kwargs={'pk': self.post_1.id})
        responce = self.client.get(url)

        post_upvoted = Post.objects.get(id=self.post_1.id).upvoted

        self.assertEqual(status.HTTP_200_OK, responce.status_code)
        self.assertEqual(1, post_upvoted)


class CommentApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.post = Post.objects.create(
            title='post1_oo',
            link='https://google.com',
            author_name='TestAuthor',
            upvoted=0,
            created=timezone.now,
        )
        self.comment_1 = Comment.objects.create(
            post=self.post,
            author_name='comment_f_author',
            content='comment1_content',
            created=timezone.now,
        )
        self.comment_2 = Comment.objects.create(
            post=self.post,
            author_name='comment_b_author',
            content='comment2_content',
            created=timezone.now,
        )
        self.comment_3 = Comment.objects.create(
            post=self.post,
            author_name='comment_c_abthor',
            content='comment3_content',
            created=timezone.now,
        )

    def test_get(self):
        url = reverse('comment-list')
        response = self.client.get(url)

        serializer_data = CommentSerializer([self.comment_1, self.comment_2, self.comment_3], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_filter(self):
        url = reverse('comment-list')
        response = self.client.get(url, data={'author_name': 'comment_f_author'})

        serializer_data = CommentSerializer(self.comment_1).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.data['results']))
        self.assertEqual(serializer_data, response.data['results'][0])

    def test_get_search(self):
        url = reverse('comment-list')
        response = self.client.get(url, data={'search': 'aut'})

        serializer_data = CommentSerializer([self.comment_1, self.comment_2], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_ordering(self):
        url = reverse('comment-list')
        response = self.client.get(url, data={'ordering': 'author_name'})

        serializer_data = CommentSerializer([self.comment_2, self.comment_3, self.comment_1], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])
