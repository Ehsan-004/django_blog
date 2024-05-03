from django.urls import path
from .views import single_post, all_posts, comment_register, post_register_page, post_register


app_name = 'blog'


urlpatterns = [
    path('article/<str:name>/', single_post, name='single_post'),
    path('articles/', all_posts, name='all_posts'),
    path('new-comment/', comment_register, name='comment_register'),
    path('new-post/',  post_register_page, name='new-post'),
    path('register_post', post_register, name='register_post'),
]
