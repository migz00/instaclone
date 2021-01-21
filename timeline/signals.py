from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from timeline.models import Post, Follow, Stream

@receiver(post_save, sender=Post)
def add_post(sender, instance, *args, **kwargs):
    	post = instance
    	user = post.user
    	followers = Follow.objects.all().filter(following=user)
    	for follower in followers:
    		stream = Stream(post=post, user=follower.follower, date=post.posted, following=user)
    		stream.save()