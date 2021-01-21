from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator


from .forms import SignupForm, EditProfileForm, EditUsernameForm
from .models import Profile
from timeline.models import Post, Follow, Stream
from django.contrib.auth.models import User

# Create your views here.
def UserProfile(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)
	
	posts = Post.objects.filter(user=user).order_by('-posted')

	post_count = Post.objects.filter(user=user).count()
	following_count = Follow.objects.filter(follower=user).count()
	follower_count = Follow.objects.filter(following=user).count()

	follow_status = Follow.objects.filter(following=user, follower=request.user).exists()
	
	context = {
		'profile' : profile,
		'posts' : posts,
		'post_count' : post_count,
		'following_count' : following_count,
		'follower_count' : follower_count,
		'follow_status' : follow_status,
	}

	return render(request, 'profile.html', context)

def Signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			User.objects.create_user(username=username, email=email, password=password)
			return redirect('index')
	else:
		form = SignupForm()
	
	context = {
		'form':form,
	}

	return render(request, 'signup.html', context)

@login_required
def follow(request, username, option):
	user = request.user
	following = get_object_or_404(User, username=username)

	try:
		fw, created = Follow.objects.get_or_create(follower=user, following=following)

		if int(option) == 0:
			fw.delete()
			Stream.objects.filter(following=following, user=user).all().delete()
		else:
			posts = Post.objects.all().filter(user=following)[:10]

			with transaction.atomic():
				for post in posts:
					stream = Stream(post=post, user=user, date=post.posted, following=following)
					stream.save()
		return HttpResponseRedirect(reverse('profile', args=[username]))
	except ObjectDoesNotExist:
		return HttpResponseRedirect(reverse('profile', args=[username]))

@login_required
def EditProfile(request):
	user = request.user.id
	profile = Profile.objects.get(user__id=user)

	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES)

		if form.is_valid():
			profile.picture = form.cleaned_data.get('picture')
			profile.first_name = form.cleaned_data.get('first_name')
			profile.last_name = form.cleaned_data.get('last_name')

			profile.save()

			return redirect('index')
	else:
		form = EditProfileForm()

	context = {
		'form':form,
	}

	return render(request, 'edit_profile.html', context)

@login_required
def UserSearch(request):
	query = request.GET.get("q")

	context = {}

	if query:
		users = User.objects.filter(Q(username__icontains=query))
		
		paginate = Paginator(users, 10)
		page_num = request.GET.get('page')
		users_paginate = paginate.get_page(page_num)

		context = {
			'users' : users_paginate,
		}
	
	return render(request, 'search_user.html', context)

