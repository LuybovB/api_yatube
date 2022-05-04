from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=200)
    slug = models.SlugField(verbose_name='Идентификатор', unique=True)
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return {self.title}


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст поста',
        help_text='Введите текст поста'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',
        blank=True, null=True,
        help_text='Выберите группу'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Автор',
        null=True,
    )
    image = models.ImageField(
        verbose_name='Картинка',
        help_text='Выберите картинку',
        upload_to='posts/',
        blank=True
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.SET_NULL,
        related_name='comments',
        verbose_name='Пост',
        blank=True, null=True,
        help_text='Пост, к которому относится комментарий'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='comments',
        verbose_name='Автор',
        null=True,
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Введите текст комментария'
    )
    created = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    def __str__(self):
        return self.text[:20]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='follower',
        verbose_name='Пользователь',
        null=True,
    )
    following = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='following',
        verbose_name='Автор',
        null=True,
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('following', 'user'), name='unique_following'),
        )

    def __str__(self):
        return f'{self.user} подписан на {self.following}'
