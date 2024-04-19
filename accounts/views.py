from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from .models import Profile, Item, FavoriteItem, Follow
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from products.models import Product, Like
# 회원가입 뷰


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'signup.html')

# 로그인 뷰


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "유효하지 않은 사용자 이름 혹은 비밀번호입니다.")
    return render(request, 'signin.html')

# 로그아웃 뷰


def signout(request):
    logout(request)
    return redirect('home')

#프로필페이지 뷰
def profile(request, username):
    user = get_object_or_404(User, username=username)
    items = Product.objects.filter(owner=user)
    favorites = Like.objects.filter(user=user).select_related('product')
    followers = user.followers.count()
    following = user.following.count()
    context = {
        'user': user,
        'items': items,
        'favorites': [like.product for like in favorites],
        'followers': followers,
        'following': following,
    }
    return render(request, 'profile.html', context,)


#팔로우 뷰
@login_required
@require_POST
def follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    return redirect('profile', username=username)