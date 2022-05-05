from rest_framework import serializers, validators
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Post, Group, Follow, User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault())
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all())

    def validate_following(self, attrs):
        if attrs == self.context['request'].user:
            raise serializers.ValidationError('Нельзя подписываться на себя!')
        return attrs

    class Meta:
        model = Follow
        fields = '__all__'

    validators = [
        validators.UniqueTogetherValidator(
            queryset=Follow.objects.all(),
            fields=['user', 'following'],
            message='Подписка уже существует.'
        )
    ]
