from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User 
from captcha.fields import CaptchaField


# Добавление задачи + категории

class AddTaskForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(AddTaskForm, self).__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Category not selected"
        self.fields['completed'].label = 'Completed-'
        self.fields['cat'].queryset = Category.objects.filter(user=user)
        

    class Meta:
        model = Task
        fields = ['title', 'slug', 'description', 'completed', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'form-control', 'placeholder': 'Description'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL', 'style': 'width:50%'}),
            'cat': forms.Select(attrs={'class': 'form-select'})
            }


class AddCategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL', 'style': 'width:50%'})

        }


# Форма удаления категории

class DeleteCategoryForm(forms.Form):
    choice_field = forms.ModelChoiceField(queryset=Category.objects.none(), label='Category', empty_label = "Not chosen", widget=forms.Select(attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(DeleteCategoryForm, self).__init__(*args, **kwargs)
        self.fields['choice_field'].queryset = Category.objects.filter(user=user)

# Форма фильтрации

class TaskFilterForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.none(), required=False, label='Category', empty_label = "Doesn't matter", widget=forms.Select(attrs={'class':'form-control'}))
    completed = forms.NullBooleanField(required=False, widget=forms.RadioSelect(choices=[
            (None, "All"),
            (True, 'Completed'),
            (False, 'Uncompleted')
        ] ))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TaskFilterForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['category'].queryset = Category.objects.filter(user=user.id)



# Форма обратной связи

class ContactForm(forms.Form):
    name = forms.CharField(label='' ,max_length=50 ,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}))
    email = forms.EmailField(label='' ,required=True ,widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}))
    message = forms.CharField(label='' ,widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your message'}))
    captcha = CaptchaField()


# Форма регистрации + авторизации

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class':'form-control',  }))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control' }))
    password2 = forms.CharField(label='Password again', widget=forms.PasswordInput(attrs={'class':'form-control' }))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class':'form-control',  }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control' }))


class ProfileEditForm(UserChangeForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class':'form-control',  }))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('username', 'email')