from django.urls import path
from .views import index, newPost, postDetails, like


urlpatterns = [
    path('', index, name='index'),
    path('newpost/', newPost, name='newpost'),
    path('<uuid:post_id>', postDetails, name='postdetails'),
    path('<uuid:post_id>/like', like, name='postlikes'),
]