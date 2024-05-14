from django.shortcuts import render, reverse, redirect
from django.views.decorators.http import require_POST
from .models import Post, Comments, Category, RecentArticles  # models
from datetime import datetime
from account.models import User
from django.contrib.auth.hashers import check_password  # to check password by hashing it
from .forms import NewPostForm  # form to add new blog


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
            # now we have a list of json dictionaries
        recent_articles = Post.recent_posts.all()  # this is a customized manager
        category_name_count = {}
        categories = Category.objects.all()

        for category in categories:
            category_name_count[category.name] =  Post.objects.filter(category__name=category.name).count()

        context = {
            'article_data': article_data,
            'latest_articles': recent_articles,
            'categories_details': category_name_count,
            'categories': categories,

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


@require_POST
def comment_register(req):
    """
    It receives data of a comment and render them on the comment page.
    first check if all data are ok, then checks if user exists and if not it
    goes to login page.
    """
    author = email = name_of_author = password = False
    # first get all data of the post to set comment
    sit = req.POST.get('situation')
    content = req.POST.get('comment_content', False)
    title_of_post = req.POST.get('title_of', False)

    # recognize the post
    the_post = Post.objects.get(title=title_of_post)

    # in single.html if user is authenticated , sit will be True else sit will be false.
    # if sit is true, in the post page there is no need to enter username and password,
    # but if sit is false it means user is not logged in and to leave a comment user should enter his/her
    # username and password and email first .
    if sit:
        name_of_author = req.POST.get('comment_author')
        try:
            author = User.objects.get(username=name_of_author)  # check if user already exists in database\
        except User.DoesNotExist:
            context = {
                'text_error': "We couldn't find the you !",
                'account': False,
                'post_name': the_post.title,
            }
            return render(req, 'error_manager.html', context)
    else:
        email = req.POST.get('email', False)
        name_of_author = req.POST.get('comment_author', False)
        password = req.POST.get('password', False)
        temp_user = User.objects.get(username=name_of_author)  # check if user already exists in database\
        # because django hashes passwords they must hash first and then check !
        if check_password(password, temp_user.password):  # prove that it is the user
            author = temp_user
        else:
            context = {
                'text_error': 'Wrong password!',
                'account': False,
                'post_name': the_post.title,
            }
            return render(req, 'error_manager.html', context)

    # check if all data is ok and not empty or not False
    print([title_of_post, content, author])
    if not False in [title_of_post, content, author]:
        try:
            comment = Comments(author=author,
                               content=content,
                               date_added=datetime.now(),
                               post=the_post)  # create new comment
            comment.save()
            # get back to the article and see your comment!
            return redirect(reverse('blog:single_post', args=[title_of_post]))
        except:
            context = {
                'text_error': 'Something went wrong!',
                'account': False,
                'post_name': the_post.title,
            }
            return render(req, 'error_manager.html', context)


def post_register(req):
    """
    if method is GET goes to the new post page
    else if method is POST goes To add new post by a user.
    It first receives data of a post like title, author, summary, and category,
    then it renders them on the post page.
    you can see new post on the index page!
    """
    if req.method == 'GET':
        return render(req, 'add post.html', {'form': NewPostForm()})
    elif req.method == 'POST':
        title = req.POST.get('title', False)
        summary = req.POST.get('summary', False)
        content = req.POST.get('content', False)
        author_name = req.POST.get('author', False)
        category_num = req.POST.get('category', False)

        if not False in [title, content, author_name, category_num]:
            if not summary:
                summary = f"a new post about {title} by {author_name}"
            try:
                user = User.objects.get(username=author_name)
                post = Post(
                    title=title,
                    content=content,
                    author=user,
                    category=Category(pk=int(category_num)),
                    summary=summary
                )
                post.save()
                return redirect(reverse('blog:all_posts'))
            except User.DoesNotExist:
                return redirect(reverse('home'))


def category_posts(req, category_name: str):
    articles_data = []
    posts_in_category = Post.objects.filter(category__name=category_name)

    for post in posts_in_category:
        articles_data.append({
            'title': post.title,
            'summary': post.summary,
            'author': post.author,
            'date': post.date,
        })
    context = {
        'category_name': category_name,
        'articles_data': articles_data,
               }
    return  render(req, 'articles_in_category.html', context)



