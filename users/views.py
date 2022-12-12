from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import SignupForm, EditProfileForm, UpdateProfileForm, UploadBlogForm, EditBlogsForm
from .models import Posts, Profile, Comments


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

    p = Paginator(blogs, 2) 
    page_number = request.GET.get('page')

    try:
        page_obj = p.get_page(page_number)

    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    

    if request.method == 'POST':
        get_response = request.POST.get('response')
        get_commentObj = request.POST.get('comment')
        get_postId = request.POST.get('posted_blog_id')


        get_BlogObj = Posts.objects.get(id=get_response, blogger=request.user.profile)
        get_BlogObj.delete()
        messages.error(request, 'Blog has been deleted successfully!')
        
        try:
            blog_obj = Posts.objects.get(id=get_postId)
            if get_commentObj != "":
                new_comment = Comments.objects.create(post=blog_obj, comment=get_commentObj, name=request.user.profile)
                new_comment.save()
        
        except Posts.DoesNotExist:
            return redirect('homepage')


        return redirect('homepage')

    context = {
        'total_blogs': Posts.objects.filter(blogger=request.user.profile).count(),
        'comments': Comments.objects.all(),

        # pagination
        'page': page_obj, 'posted_blogs': page_obj        
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

@login_required(login_url='login')
@user_passes_test(lambda user: user.is_staff is False and user.is_superuser is False)
def viewuserprofile_view(request, user_name):
    obj = User.objects.get(username=user_name)


    
    context = {'obj':obj, }
    return render(request, 'users/view_profile.html', context)


class LogoutUser(LogoutView):
    template_name = 'users/logout.html'