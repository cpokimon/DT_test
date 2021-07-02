from django.views.generic import ListView, DetailView
from django.shortcuts import redirect, render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Comment
from .forms import CommentForm


class PostListView(ListView):
    model = Post
    paginate_by = 5
    queryset = Post.objects.all()
    ordering = ['id']
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


def post_comment_create_view(request, pk):
    template = 'create_comment.html'
    form = CommentForm(request.POST)
    if form.is_valid():
        form.cleaned_data['post_id'] = pk
        form.save()
        return redirect('post_detail', pk=pk)
    context = {"form": form}
    return render(request, template, context)


def upvote_post_view(request, pk=None):
    try:
        post = Post.objects.get(id=pk)
        post.upvote()
        post.save()
    except Post.DoesNotExist:
        return redirect('home')
    else:
        return redirect('post_detail', pk=pk)


@api_view()
def upvoute_post_api(request, pk=None):
    post = get_object_or_404(Post, id=pk)
    post.upvote()
    post.save()
    return Response({"detail": "Upvouted."}, status.HTTP_200_OK)
