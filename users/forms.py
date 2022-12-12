from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Posts


class SignupForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

class UpdateProfileForm(forms.ModelForm):
    CHOICE_GENDER = (
        (None, '-- Select Gender --'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = forms.ChoiceField(widget=forms.Select(attrs={'type': 'select', 'class': 'mb-2'}), choices=CHOICE_GENDER)
    dob = forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'mb-2'}))
    phone_no = forms.CharField(widget=forms.TextInput(attrs={'type': 'tel', 'class': 'mb-2'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'type': 'text',  'class': 'mb-2'}))

    class Meta:
        model = Profile
        fields = ['gender', 'dob', 'phone_no', 'country', 'dp']


class EditProfileForm(forms.ModelForm):
    CHOICE_GENDER = (
        (None, '-- Select Gender --'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = forms.ChoiceField(widget=forms.Select(attrs={'type': 'select', 'class': 'mb-2'}), choices=CHOICE_GENDER, disabled=True)
    phone_no = forms.CharField(widget=forms.TextInput(attrs={'type': 'tel', 'class': 'mb-2'}), disabled=True)
    country = forms.CharField(widget=forms.TextInput(attrs={'type': 'text',  'class': 'mb-2'}), disabled=True)

    class Meta:
        model = Profile
        fields = ['gender', 'phone_no', 'country', 'dp']


class UploadBlogForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'placeholder': 'Enter title ...'}), help_text='Title of your blog should contain atleast 60 characters')
    content = forms.CharField(widget=forms.Textarea(attrs={'type': 'text', 'placeholder': 'What\'s on your mind today ...?'}))

    class Meta:
        model = Posts
        fields = ['title', 'content']

class EditBlogsForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'type': 'text'}), help_text='Title of your blog should contain atleast 60 characters')
    content = forms.CharField(widget=forms.Textarea(attrs={'type': 'text'}))

    class Meta:
        model = Posts
        fields = ['title', 'content']