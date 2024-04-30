from django.shortcuts import render, reverse, redirect
from .models import Post, Comments


def index(req):
    if req.method == 'GET':
        article_data = []
        articles = Post.objects.all()
        for article in articles:
            article_data.append({
                'title': article.title,
                'summary': article.summary,
                'author': article.author,
                'date': article.date,
            })
        context = {
            'article_data': article_data
        }
        return render(req, 'index.html', context)


def single_post(req, name: str):
    articles = Post.objects.all()  # all articles are here
    for article in articles:
        if article.title == name:
            comment_list = []
            comments = Comments.objects.filter(post=article)  # get its comments
            comments_num = len(comments)
            for comment in comments:
                comment_list.append({
                    'content': comment.content,
                    'author': comment.author,
                })

            context = {
                'title': article.title,
                'summary': article.summary,
                'author': article.author,
                'date': article.date,
                'content': article.content,
                'comments': article.comments,
                'category': article.category,
                'comment_list': comment_list,
                'comments_num': comments_num,
            }
            return render(req, 'single.html', context)
    return render(req, redirect(reverse('blog:all_posts')))


def all_posts(req):
    if req.method == 'GET':
        articles = []
        articles_data = Post.objects.all()
        for article in articles_data:
            articles.append({
                'title': article.title,
                'summary': article.summary,
                'author': article.author,
                'date': article.date,
            })
        return render(req, 'articles_page.html', {'articles_data': articles_data})
