from django import forms
from .models import Comment, Post


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author_name', 'content')

    def clean_post_id(self):
        return self.cleaned_data['post_id']

    def clean_created(self):
        return None

    def save(self):
        data = self.cleaned_data
        post = Post.objects.get(id=data['post_id'])
        if post:
            comment = Comment()
            comment.author_name = data['author_name']
            comment.post = post
            comment.content = data['content']
            comment.save()
