from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    link = models.CharField(max_length=2048)
    author_name = models.CharField(max_length=255, blank=False, null=False)
    upvoted = models.IntegerField(default=0)
    created = models.DateField(editable=False, auto_now_add=True)

    def __str__(self):
        return f'ID:{self.id}, TITLE:{self.title[:10]}'


class Comment(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    author_name = models.CharField(max_length=255, null=False, blank=False)
    content = models.TextField()
    created = models.DateField(editable=False, auto_now_add=True)

