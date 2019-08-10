from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) #creqte a form that hase request.POST data
        if form.is_valid(): #same username pw naileko validation garney kam garcha
            form.save()
            username = form.cleaned_data.get('username') #validated form data will be in cleaned_data dictionary
            messages.success(request, f'Account created for {username}!')
            return redirect('login') #name for blog homepage
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required()
def profile(request):
    # if request.method == 'POST':
    #     u_form = UserUpdateForm(request.POST, instance=request.user)
    #     p_form = ProfileUpdateForm(request.POST,
    #                                request.FILES,
    #                                instance=request.user.profile)
    #     if u_form.is_valid() and p_form.is_valid():
    #         u_form.save()
    #         p_form.save()
    #         messages.success(request, f'Your Account has been updated')
    #         return redirect('profile')
    #
    # else:
    #     u_form = UserUpdateForm(instance=request.user)
    #     p_form = ProfileUpdateForm(instance=request.user.profile)
    #
    # context = {
    #     'u_form': u_form,
    #     'p_form': p_form,
    # }
    # return render(request, 'users/profile.html', context)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your Account has been updated')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
    }
    return render(request, 'users/profile.html', context)









