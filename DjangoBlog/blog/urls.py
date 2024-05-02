from django.urls import path
from .views import single_post, all_posts, comment_register
from django.shortcuts import render, reverse, redirect


app_name = 'blog'


urlpatterns = [
    path('article/<str:name>/', single_post, name='single_post'),
    path('articles/', all_posts, name='all_posts'),
    path('new-comment/', comment_register, name='comment_register'),
]
