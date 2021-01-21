from django.urls import path
from .views import Signup, EditProfile, UserSearch

from django.contrib.auth import views as authViews 



urlpatterns = [

    path('profile/edit', EditProfile, name='edit-profile'),
    path('signup/', Signup, name='signup'),
   	path('login/', authViews.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', authViews.LogoutView.as_view(), {'next_page' : 'index'}, name='logout'),
    path('search/', UserSearch, name='usersearch'),

]