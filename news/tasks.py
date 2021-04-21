from django.db import transaction
from .models import Post
from project.celery import app as celery_app


@celery_app.task(name='reset_upvoutes')
def reset_upvoutes():
    posts = Post.objects.all()
    with transaction.atomic():
        for post in posts:
            post.upvoted = 0
            post.save()