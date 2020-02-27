from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)


@login_required
def follow(request, pk):
    user_profile = Profile.objects.get(user=request.user)
    to_follow_profile = Profile.objects.get(pk=pk)

    if user_profile != to_follow_profile:
        user_profile.following.add(to_follow_profile.user)
        to_follow_profile.followers.add(user_profile.user)

    return redirect('/blog/user/{}/'.format(to_follow_profile.user.username))
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/blog/'))


@login_required
def un_follow(request, pk):
    user_profile = Profile.objects.get(user=request.user)
    to_un_follow_profile = Profile.objects.get(pk=pk)

    user_profile.following.remove(to_un_follow_profile.user)
    to_un_follow_profile.followers.remove(user_profile.user)

    return redirect('/blog/user/{}/'.format(to_un_follow_profile.user.username))
