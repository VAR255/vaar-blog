from rest_framework import serializers
from blog.models import Comment, Post
from django.contrib.auth.models import User



ACTIONS_OPTIONS_VALUE = ["like", "unlike"]



class CommentLikes(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in ACTIONS_OPTIONS_VALUE:
            raise serializers.ValidationError("the action is not found")
        return value




class StringSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value

# class ParentCommentSerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = Comment
    #     fields = ['parent', 'post', 'content',]

class CommentSerializer(serializers.ModelSerializer):
    parent = StringSerializer(many=False)
    author = StringSerializer(many=False)
    profile = StringSerializer(many=False)
    likes_comment = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'likes_comment', 'post', 'content', 'parent', 'author', 'publish', 'profile',]
    
    def get_likes_comment(self, obj):
        return obj.likes_comment.count()
    
   
    


