from django.shortcuts import render
from . serializers import CommentSerializer
from blog.models import Comment, Post

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from blog_api.serializers import CommentLikes

# Create your views here.
@api_view(["GET"])
def comment_api_views(request, id):
    post = Post.objects.get(id=id)
    all_comment = Comment.objects.filter(post=post).order_by('-id')
    serializer = CommentSerializer(all_comment, many=True)
    return Response(serializer.data, status=200)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def comment_api_create(request, id):
    serializer = CommentSerializer(data=request.POST)
    print(serializer.is_valid())
    if serializer.is_valid(raise_exception=True):
        serializer.save(author=request.user)
        return Response(serializer.data, status=201)
    return Response(status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_comment_like_api(request, *args, **kwargs):
    serializer = CommentLikes(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        comment_id = data.get("id")
        action = data.get("action")
        qs = Comment.objects.filter(id=comment_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        print(obj)
        if action == "like":
            obj.likes_comment.add(request.user)
            serializer = CommentSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes_comment.remove(request.user)
            serializer = CommentSerializer(obj)
            return Response(serializer.data, status=200)
    return Response({}, status=400)
