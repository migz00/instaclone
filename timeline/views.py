from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Post, Stream, Likes, Comment

from .forms import NewPost, CommentForm

# Create your views here.
@login_required
def index(request):
    user = request.user
    posts = Stream.objects.filter(user=user)
    

    posts_id = []
    liked = []

    for post in posts:
        posts_id.append(post.post_id)

    post_items = Post.objects.filter(id__in=posts_id).all().order_by('-posted')

    for post in post_items:
        liked = Likes.objects.filter(user=user, post=post).count()
        if liked:
            post.liked = True
        else:
            post.liked = False


    context = {
		'post_items':post_items,
	}

    return render(request, 'index.html', context)

@login_required
def postDetails(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    liked = Likes.objects.filter(user=request.user, post=post).count()

    comments = Comment.objects.filter(post=post).order_by('date')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            
            return HttpResponseRedirect(reverse('postdetails', args=[post_id]))
    else:
        form = CommentForm()


    if liked:
        post.liked = True
    else:
        post.liked = False

    context = {
        'post' : post,
        'comments' : comments,
        'form' : form,
    }

    return render(request, 'post_detail.html', context)

@login_required
def newPost(request):
    user = request.user.id

    if request.method == 'POST':
        form = NewPost(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')

            o, created = Post.objects.get_or_create(picture=picture, caption=caption, user_id=user)
            o.save()
            return redirect('index')
        
    else:
        form = NewPost()
    
    context = {
        'form': form,
    }

    return render(request, 'newpost.html', context)

@login_required
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes

    liked = Likes.objects.filter(user=user, post=post).count()

    if not liked:
        like = Likes.objects.create(user=user, post=post)
        current_likes = current_likes + 1
    else:
        Likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1

    post.likes = current_likes
    post.save()

    return HttpResponseRedirect(reverse('postdetails', args=[post_id]))