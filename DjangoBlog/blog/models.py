from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from account.models import Account
from django_quill.fields import QuillField


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
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # tags = models.ManyToManyField(Tag, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    seen_num = models.IntegerField(default=0)
    comment = models.ForeignKey('comments', on_delete=models.CASCADE,
                                related_name='post_comments', null=True, blank=True)
    date = models.DateTimeField(default=now)
    summary = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'posts'
        verbose_name = 'posts'
        verbose_name_plural = 'posts'


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'comments'
        verbose_name = 'comments'
        verbose_name_plural = 'comments'


# class Tag(models.Model):
#     CH = [
#         ('python', 'Python'),
#         ('java', 'Java'),
#         ('javascript', 'JavaScript'),
#         ('c++', 'C++'),
#         ('ruby', 'Ruby'),
#         ('swift', 'Swift'),
#         ('go', 'Go'),
#         ('html', 'HTML'),
#         ('css', 'CSS'),
#         ('php', 'PHP'),
#         ('angular', 'Angular'),
#     ]
#     tag_name = models.CharField(max_length=20, choices=CH, null=True, blank=True)
#
#     def __str__(self):
#         return self.tag_name
#
#     class Meta:
#         db_table = 'tag'
#         verbose_name = 'tag'
#         verbose_name_plural = 'tags'
