from django.contrib import admin
from blog.models import Post, Category, Comments


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'date_added')


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comments, CommentsAdmin)
