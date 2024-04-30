from django.urls import path
from .views import single_post, all_posts


app_name = 'blog'


urlpatterns = [
    path('article/', single_post),
    path('articles/', all_posts, name='all_posts'),
]
