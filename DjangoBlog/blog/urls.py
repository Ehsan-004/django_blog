from django.urls import path
from .views import single_post, all_posts, comment_register, post_register, category_posts


app_name = 'blog'


urlpatterns = [
    path('article/<str:name>/', single_post, name='single_post'),  # opens an article singly
    path('articles/', all_posts, name='all_posts'),  # it shows all articles
    path('new-comment/', comment_register, name='comment_register'),  # to leave new comment
    path('new-post/',  post_register, name='register_post'),  # goes to the adding new post page
    path('catogory/<str:category_name>/', category_posts, name='category_posts'),
]
