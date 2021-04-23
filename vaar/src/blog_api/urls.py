from django.urls import path
from . views import comment_api_views, comment_api_create
from blog_api.views import create_comment_like_api

app_name = "blog_api"

urlpatterns = [
    path('comment/<str:id>', comment_api_views, name="comment"),
    path('create/comment/<str:id>', comment_api_create, name="create-comment"),
    path('action/', create_comment_like_api, name='action'),
]
