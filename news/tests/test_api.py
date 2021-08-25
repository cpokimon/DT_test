import json

from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
from django.urls import reverse
from ..models import Post, Comment
from ..serializers import PostSerializer, CommentSerializer
from django.utils import timezone
from django.contrib.auth.models import User
from ..viewsets import PostViewSet


class PostsApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
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
        self.user = User.objects.create_user(username='test_user', email='t@e.st', password='test_password')

    def test_get_authorized_unauthorized(self):
        url = reverse('post-list')
        response = self.client.get(url)

        serializer_data = PostSerializer([self.post_1, self.post_2, self.post_3], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

        self.client.force_login(self.user)
        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_filter_authorized_unauthorized(self):
        url = reverse('post-list')
        response = self.client.get(url, data={'title': 'post1_oo'})

        serializer_data = PostSerializer(self.post_1).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.data['results']))
        self.assertEqual(serializer_data, response.data['results'][0])

        self.client.force_login(user=self.user)
        response = self.client.get(url, data={'title': 'post1_oo'})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.data['results']))
        self.assertEqual(serializer_data, response.data['results'][0])

    def test_get_search_authorized_unauthorized(self):
        url = reverse('post-list')
        response = self.client.get(url, data={'search': 'oo'})

        serializer_data = PostSerializer([self.post_1, self.post_2], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

        self.client.force_login(user=self.user)
        response = self.client.get(url, data={'search': 'oo'})

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_ordering_authorized_unauthorized(self):
        url = reverse('post-list')
        response = self.client.get(url, data={'ordering': '-author_name'})

        serializer_data = PostSerializer([self.post_3, self.post_1, self.post_2], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

        self.client.force_login(user=self.user)
        response = self.client.get(url, data={'ordering': '-author_name'})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_upvote_post_authorized(self):
        self.client.force_login(user=self.user)
        url = reverse('post_upvote', kwargs={'pk': self.post_1.id})
        response = self.client.get(url)

        post_upvoted = Post.objects.get(id=self.post_1.id).upvoted

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, post_upvoted)

    def test_upvote_post_unauthorized(self):
        url = reverse('post_upvote', kwargs={'pk': self.post_1.id})
        response = self.client.get(url)
        self.assertEqual(403, response.status_code)

    def test_create_authorized(self):
        url = reverse('post-list')
        data = {
            "title": "TestTitle",
            "link": "https://google.com",
            "author_name": "TestAuthor",
        }
        self.client.force_login(self.user)
        response = self.client.post(path=url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(201, response.status_code)
        self.assertTrue(Post.objects.filter(**data).exists())

    def test_create_unauthorized(self):
        url = reverse('post-list')
        data = {
            "title": "TestTitle",
            "link": "https://google.com",
            "author_name": "TestAuthor",
        }
        response = self.client.post(path=url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(403, response.status_code)

    def test_update_authorized_unauthorized(self):
        url = reverse('post-list')
        data = {
            "title": "TUPtestTitle",
            "author_name": "ShallowRat",
        }
        request = self.factory.put(url, data=data, format='json')
        view = PostViewSet.as_view({'put': 'update'})

        response = view(request, pk=self.post_1.id)
        self.assertEqual(403, response.status_code)

        force_authenticate(request, user=self.user)

        response = view(request, pk=self.post_1.id)
        self.post_1.refresh_from_db()
        self.assertEqual(200, response.status_code)
        self.assertEqual("TUPtestTitle", self.post_1.title)

    def test_partial_update_authorized_unauthorized(self):
        url = reverse('post-list')
        data = {
            "title": "TestPPU",
        }

        request = self.factory.patch(url, data=data, format='json')
        view = PostViewSet.as_view({'patch': 'update'})

        response = view(request, pk=self.post_1.id)
        self.assertEqual(403, response.status_code)

        force_authenticate(request, self.user)

        response = view(request, pk=self.post_1.id, partial=True)
        self.post_1.refresh_from_db()
        self.assertEqual(200, response.status_code)
        self.assertEqual("TestPPU", self.post_1.title)


class CommentApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
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
        self.user = User.objects.create_user(username='test_user', email='t@e.st', password='test_password')

    def test_get_authorized_unauthorized(self):
        url = reverse('comment-list')
        response = self.client.get(url)

        serializer_data = CommentSerializer([self.comment_1, self.comment_2, self.comment_3], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

        self.client.force_login(user=self.user)

        response = self.client.get(url)
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

    def test_create_authorized_unauthorized(self):
        url = reverse('comment-list')
        data = {
            "title": "TestTitle",
            "link": "https://google.com",
            "author_name": "TestAuthor",
            "content": "random_content",
        }
        serialized_data = CommentSerializer(data=data)
        serialized_data.is_valid()
        serialized_data = serialized_data.data
        response = self.client.post(path=url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

        self.client.force_login(self.user)
        response = self.client.post(path=url, data=json.dumps(data), content_type='application/json')
        print(response.data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        # self.assertEqual(serialized_data, response.data['results'])

