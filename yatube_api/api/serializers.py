from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    CurrentUserDefault, ModelSerializer, SlugRelatedField)
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post, User

VALIDATION_ERROR_MESSAGE = ('Отсутствует обязательное поле в теле запроса или'
                            ' оно не соответствует требованиям')


class BaseAuthorSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'


class PostAuthorSerializer(BaseAuthorSerializer):
    class Meta(BaseAuthorSerializer.Meta):
        model = Post


class CommentAuthorSerializer(BaseAuthorSerializer):
    class Meta(BaseAuthorSerializer.Meta):
        model = Comment
        read_only_fields = ('post',)


class GroupSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(ModelSerializer):
    user = SlugRelatedField(
        slug_field='username', read_only=True, default=CurrentUserDefault())
    following = SlugRelatedField(
        slug_field='username', queryset=User.objects.all())

    class Meta:
        fields = ('user', 'following')
        model = Follow
        validators = (
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message=VALIDATION_ERROR_MESSAGE
            ),
        )

    def validate_following(self, value):
        if value == self.context['request'].user:
            raise ValidationError(VALIDATION_ERROR_MESSAGE)
        return value
