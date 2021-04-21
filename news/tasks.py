from django.db import transaction
from .models import Post
from celery.task import periodic_task
from datetime import timedelta


@periodic_task(run_every=timedelta(seconds=3600))
def reset_upvoutes():
    posts = Post.objects.exclude(upvoted=0)
    with transaction.atomic():
        for post in posts:
            post.upvoted = 0
            post.save()
