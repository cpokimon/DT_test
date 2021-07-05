from .models import Post
from celery.task import periodic_task
from datetime import timedelta


@periodic_task(run_every=timedelta(seconds=3600))
def reset_upvoutes():
    Post.objects.exclude(upvoted=0).update(upvoted=0)
