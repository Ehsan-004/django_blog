from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from account.models import Account
from django_quill.fields import QuillField  # quill text editor


# managers
class RecentArticles(models.Manager):
    """this is a manager for Post model that returns recent articles"""
    def get_queryset(self):
        return super().get_queryset().order_by('-date')[0:5]


# models
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = QuillField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    seen_num = models.IntegerField(default=0)
    date = models.DateTimeField(default=now)
    summary = models.CharField(max_length=150, null=True, blank=True)
    recent_posts = RecentArticles()
    objects = models.Manager()

    class Meta:
        db_table = 'posts'
        verbose_name = 'posts'
        verbose_name_plural = 'posts'


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=now)
    content = models.TextField()

    class Meta:
        db_table = 'comments'
        verbose_name = 'comments'
        verbose_name_plural = 'comments'
