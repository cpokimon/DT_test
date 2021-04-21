from django.views.generic import ListView, DetailView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Comment


class PostListView(ListView):
    model = Post
    paginate_by = 5
    queryset = Post.objects.all()
    context_object_name = 'posts'
    template_name = 'posts.html'


class PostDetailView(DetailView):
    model = Post
    slug_field = 'custom_slug_field'
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        post_id = kwargs['object'].id
        context['comments'] = Comment.objects.all().filter(post_id=post_id)
        return context


@api_view()
def upvoute_post(request, id=None):
    try:
        post = Post.objects.get(id=id)
        post.upvoted += 1
        post.save()
    except Post.DoesNotExist:
        return Response({"detail": "Not found."}, status.HTTP_404_NOT_FOUND)
    else:
        return Response({"detail": "Upvouted."}, status.HTTP_200_OK)
