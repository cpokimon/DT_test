from django.core.management.base import BaseCommand
from django.db import transaction
from news.models import Post


class Command(BaseCommand):
    help = "Resets the votes of all posts"

    def handle(self, *args, **options):
        posts = Post.objects.all()
        with transaction.atomic():
            for post in posts:
                post.upvoted = 0
                post.save()
        self.stdout.write(self.style.SUCCESS("Successfully reset"))
