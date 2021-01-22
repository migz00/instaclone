import uuid
from django.db import models
from django.contrib.auth.models import User

from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
def user_directory_path(instance, filename):
    
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Post(models.Model):
    objects = models.Manager()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(upload_to=user_directory_path, verbose_name="Picture", null=False)
    caption = models.TextField(max_length=1500, verbose_name='Caption')
    posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    def get_abs_url(self):
        return reverse('postdetails', args=[str(self.id)])

class Follow(models.Model):
    objects = models.Manager()
    follower = models.ForeignKey(User,on_delete=models.CASCADE, null=True, related_name='follower')
    following = models.ForeignKey(User,on_delete=models.CASCADE, null=True, related_name='following')

class Likes(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')

class Stream(models.Model):
    objects = models.Manager()
    following = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name='stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField()

class Comment(models.Model):
    objects = models.Manager()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


