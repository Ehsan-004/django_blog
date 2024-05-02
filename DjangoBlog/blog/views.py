from django.core.exceptions import SuspiciousOperation
from django.shortcuts import render, reverse, redirect
from .models import Post, Comments
from datetime import datetime
from account.models import User


def index(req):
    """It receives all articles and render them on the home page."""
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
    """By clicking on the name of articles in the pages, it renders the article by name."""
    articles = Post.objects.all()  # all articles are here
    for article in articles:
        if article.title == name:
            comment_list = []
            comments = Comments.objects.filter(post=article)  # get its comments
            comments_num = len(comments)
            for comment in comments:
                comment_list.append({  # data for comment
                    'content': comment.content,
                    'author': comment.author,
                    'date': comment.date_added,
                })
            context = {  # the main data
                'title_of': article.title,
                'summary': article.summary,
                'author': article.author,
                'date': article.date,
                'content': article.content,
                'comments': article.comments,
                'category': article.category,
                'comments_num': comments_num,
                'comment_list': comment_list,
            }
            return render(req, 'single.html', context)
    return render(req, redirect(reverse('blog:all_posts')))


def all_posts(req):
    """It receives all posts and render them for posts page"""
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


def comment_register(req):
    if req.method == 'POST':
        email = req.POST.get('email', False)
        content = req.POST.get('comment_content', False)
        title_of_post = req.POST.get('title_of', False)
        name_of_author = req.POST.get('comment_author', False)
        password = req.POST.get('password', False)
        # check if all data is ok and not empty or not False
        if not False in [email, title_of_post, content, name_of_author, password]:
            the_post = Post.objects.get(title=title_of_post)  # it is impossible that the post is empty.
            try:
                author = User.objects.get(username=name_of_author)  # check if user already exists in database\
                if author.password == password:  # prove that it is the user
                    comment = Comments(author=author,
                                       content=content,
                                       date_added=datetime.now(),
                                       post=the_post)  # create new comment
                    comment.save()
                    # get back to the article and see your comment!
                    return redirect(reverse('blog:single_post', args=[title_of_post]))
                else:
                    context = {
                        'text_error': 'Wrong password!',
                        'account': False,
                        'post_name': the_post.title,
                    }
                    return render(req, 'error_manager.html', context)
            except User.DoesNotExist:  # if user was not registered or username or email is wrong
                return redirect(reverse('account:signup_page'))
