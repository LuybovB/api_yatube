from posts.models import Comment, Group, Post
from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.settings import api_settings

from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        user_del = self.request.user
        instance = self.get_object()
        author = instance.author
        if user_del != author:
            raise PermissionDenied('Нельзя изменять чужое сообщение')
        serializer.save(author=self.request.user)

    def perform_destroy(self, serializer):
        user_del = self.request.user
        instance = self.get_object()
        author = instance.author
        if author != user_del:
            raise PermissionDenied('Нельзя удалить чужое сообщение')
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, *args, **kwargs):
        post_com_id = kwargs['post_id']
        queryset = self.filter_queryset(self.get_queryset())
        post_com = queryset.filter(post_id=post_com_id)
        page = self.paginate_queryset(post_com)
        if page is not None:
            serializer = self.get_serializer(page, many=True)

            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(post_com, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = Post.objects.get(id=int(post_id))
        user_cr = self.request.user
        serializer.save(author=user_cr, post=post)

    def perform_update(self, serializer):
        author = serializer.instance.author
        user_upd = self.request.user
        if author != user_upd:
            raise PermissionDenied('Нельзя изменить чужой комментарий')
        post_id = self.kwargs['post_id']
        post = Post.objects.get(id=int(post_id))
        author_upd = self.request.user
        serializer.save(author=author_upd, post=post)

    def perform_destroy(self, serializer):
        instance = self.get_object()
        author = instance.author
        user_del = self.request.user
        if author != user_del:
            raise PermissionDenied('Нельзя удалить чужой коментарий')
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
