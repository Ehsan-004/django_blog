from django.shortcuts import render
from .models import Post


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


def single_post(req):
    return render(req, 'single.html')


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
