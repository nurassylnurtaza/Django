from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth import logout


from .models import Profile, Follow

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('profile')
def logout_view(request):
    logout(request)
    return redirect('home')
def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')


        user = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.create(user=user)
        login(request, user)
        return redirect('profile')
    return render(request, 'users/registration.html')

def home_view(request):
    return render(request, 'users/home.html')
@login_required
def profile_view(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    profile = get_object_or_404(Profile, user=user)

    is_own_profile = user == request.user

    following = Follow.objects.filter(follower=user) if is_own_profile else None

    return render(request, 'users/profile.html', {
        'profile': profile,
        'is_own_profile': is_own_profile,
        'following': following,
    })
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

@login_required
def edit_profile(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)

    if request.method == 'POST':
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.save()

        profile.bio = request.POST.get('bio', profile.bio)
        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES['profile_picture']
        profile.save()

        return redirect('profile')

    return render(request, 'users/edit_profile.html', {'profile': profile})




@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if request.user != user_to_follow:
        Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    return redirect('user_list')


@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(follower=request.user, following=user_to_unfollow).first()
    if follow:
        follow.delete()
    return redirect('user_list')


@login_required
def user_list(request):
    users = User.objects.all()
    following = Follow.objects.filter(follower=request.user).values_list('following', flat=True)

    return render(request, 'users/user_list.html', {
        'users': users,
        'following': User.objects.filter(id__in=following)
    })