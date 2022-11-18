from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from .forms import SignupForm, EditProfileForm, UpdateProfileForm, UploadBlogForm, EditBlogsForm
from .models import Posts


class UserLogin(LoginView):
    template_name = 'users/login.html'


def signup_view(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, 'Account created successfully!')
            return redirect('profile')

    context = {'signup_form': form}
    return render(request, 'users/signup.html', context)


@login_required(login_url='login')
@user_passes_test(lambda user: user.is_staff is False and user.is_superuser is False)
def userprofile_view(request):
    edit_form = EditProfileForm(instance=request.user.profile)
    update_form = UpdateProfileForm(instance=request.user.profile)

    if request.method == 'POST':
        update_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        edit_form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, 'Profile edited successfully!')
            
        elif edit_form.is_valid():
            edit_form.save()
            messages.info(request, 'Profile picture updated successfully!')
        
        return redirect('profile')


    context = {'edit_profile': edit_form, 'update_profile': update_form}
    return render(request, 'users/profile.html', context)


@login_required(login_url='login')
@user_passes_test(lambda user: user.is_staff is False and user.is_superuser is False)
def homepage_view(request):
    blogs = Posts.objects.all()

    if request.method == 'POST':
        get_response = request.POST['response']
        
        get_BlogObj = Posts.objects.get(id=get_response, blogger=request.user.profile)
        get_BlogObj.delete()
        
        messages.error(request, 'Blog has been deleted successfully!')

        return redirect('homepage')

    context = {
        'posted_blogs': blogs, 'total_blogs': Posts.objects.filter(blogger=request.user.profile).count(),

    }
    return render(request, 'users/index.html', context)


@login_required(login_url='login')
@user_passes_test(lambda user: user.is_staff is False and user.is_superuser is False)
def blogging_view(request):
    blog_form = UploadBlogForm()

    if request.method == 'POST':
        blog_form = UploadBlogForm(request.POST, )
        
        if blog_form.is_valid():
            form = blog_form.save(commit=False)
            form.blogger = request.user.profile
            form.save()
            print(f'Instance: {form.blogger} | Posted: {form.posted}')
            messages.success(request, 'Blog posted successfully!')
            return redirect('homepage')

    context = {'post_blog': blog_form}
    return render(request, 'users/upload.html', context)


@login_required(login_url='login')
@user_passes_test(lambda user: user.is_staff is False and user.is_superuser is False)
def editblogs_view(request, pk, name):
    obj = Posts.objects.get(id=pk)
    edit_blog = EditBlogsForm(instance=obj)

    if request.method == 'POST':
        edit_blog = EditBlogsForm(request.POST, instance=obj)

        if edit_blog.is_valid():
            form = edit_blog.save(commit=False)
            form.save()
            messages.warning(request, f'You have edited blog "{form.title}"')
            return redirect('edit_blog', pk, name)


    context = {'edit_blog': edit_blog,}
    return render(request, 'users/edit.html', context)


class LogoutUser(LogoutView):
    template_name = 'users/logout.html'