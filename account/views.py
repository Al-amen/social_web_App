from django.shortcuts import render, redirect,get_object_or_404
from account.forms import RegisterForm, LoginForm, ProfileForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from account.models import Profile
from django.contrib.auth.models import User
from newsfeed.models import Post

@login_required
def home(request):
    return render(request, 'newsfeed/feed.html')


def register(request):
     if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account:login')
     else:  
         form = RegisterForm()
     return render(request, 'account/register.html', {'form': form})
    
            
  
class CustomLoginView(LoginView):
    template_name = "account/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True  # Redirect if already logged in
    next_page = reverse_lazy("newsfeed:newsfeed") # Next page
  

class SettingsView(TemplateView):
      template_name = "account/settings/setting.html"

def settings(request):
    return render(request, 'account/settings/setting.html')

def profile(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    profile = get_object_or_404(Profile.objects.select_related('user'), user=user)
    posts = profile.user.posts.all().order_by('-created_at')

    return render(request, 'account/profile/profile.html', {
        "profile": profile,
        "posts": posts
    })



@login_required
def update_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('account:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'account/profile/edit_profile.html', {'form': form})




