from django.urls import path, include
from .views import signup_page, login_page, login_, register_, logout_, profile_page

app_name = 'account'


urlpatterns = [
    path('login/', login_page, name='login_page'),
    path('register/', signup_page, name='signup_page'),
    path('loggingin/', login_, name='login'),
    path('registration/', register_, name='register'),
    path('logout/', logout_, name='logout'),
    path('prifile/', profile_page, name='profile_page'),
]
