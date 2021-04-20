from rest_framework import routers
from . import viewsets


router = routers.DefaultRouter()
router.register(r'posts', viewsets.PostViewSet)
router.register(r'comments', viewsets.CommentViewSet)
