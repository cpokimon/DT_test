from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Post


@api_view()
def upvoute_post(request, id=None):
    try:
        post = Post.objects.get(id=id)
        post.upvoted += 1
        post.save()
    except Post.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_200_OK)
