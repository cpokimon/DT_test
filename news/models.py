from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=255, null=False)
    link = models.CharField(max_length=2048)
    author_name = models.CharField(max_length=255, null=False)
    upvoted = models.IntegerField(default=0)
    created = models.DateField(editable=False, auto_now_add=True)
