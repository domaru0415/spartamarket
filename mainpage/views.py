from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home(request):
    context = {'username': None}
    if request.user.is_authenticated:
        context['username'] = request.user.username
    return render(request, 'home.html', context)
