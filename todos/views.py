from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required

#Class-based views imports
from django.views import View
from django.views.generic import DetailView, UpdateView, DeleteView, ListView, CreateView, FormView


# User authentication imports 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, get_user_model


# Redirect -
from django.http import HttpResponseRedirect


# email methods
from django.core.mail import send_mail, BadHeaderError
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy


# models, forms etc.
from .forms import *
from .models import *
from .utils import *





# Превью

class PreviewContactView(FormView):
    form_class = ContactForm
    template_name = 'todos/preview.html'
    

    def form_valid(self, form):
        context = {
            'success': 'Success'
        }
        return self.render_to_response(context)




# Задачи

class TaskListView(ListView):
    model = Task
    template_name = 'todos/main.html'
    context_object_name = 'task'
    paginate_by = 5


    def get_queryset(self):
        if self.request.user.is_authenticated:                      # Вначале идет проверка на то авторизирован ли пользователь - если нет то фильтр и модель в шаблоне не передаются
            tasks = Task.objects.filter(user=self.request.user)

            form = TaskFilterForm(self.request.GET, user=self.request.user)     # Данная строка нужна для сохранения целостности формы при изменении а также передает user в форму для фильтрации поля категории 
            if form.is_valid():
                category = form.cleaned_data['category']
                completed = form.cleaned_data['completed']

                if category is not None:
                    tasks = tasks.filter(cat=category)
                if completed is not None:                           # Система ветвления на случай если поля окажутся не заполнеными и такое действие не вызвало ошибки
                    tasks = tasks.filter(completed=completed)
            return tasks
        else:
            tasks = Task.objects.none()
            return tasks

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['form'] = TaskFilterForm(self.request.GET, user=self.request.user)
            context['params'] = self.request.GET.copy()
            if 'page' in context['params']:
                del context['params']['page']        

        return context


# Выполнено/невыполнено

class CompletedView(View, DataMixin):
    model = None

    def get_object(self):
        todo_id = self.kwargs.get('todo_id')
        return Task.objects.get(id=todo_id)


    def get(self, request, *args, **kwargs):
        todo_id = kwargs.get('todo_id')
        todo = Task.objects.get(id=todo_id)
        todo.completed = not todo.completed
        todo.save()
        previous_url = request.META.get('HTTP_REFERER', 'home')
        return HttpResponseRedirect(previous_url)




# Ниже код добавления задачи + категории


# Добавление задачи

class AddTaskView(LoginRequiredMixin, CreateView):
    form_class = AddTaskForm
    template_name = 'todos/add_task.html'
    success_url = reverse_lazy('success')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user.id})
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# Добавление категории

class AddCatView(LoginRequiredMixin, CreateView):
    form_class = AddCategoryForm
    template_name = 'todos/add_cat.html'
    success_url = reverse_lazy('success')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)




# Ниже код : удаление , осмотр , редактирование


# Детальный просмотр

class TaskDetailView(LoginRequiredMixin, DataMixin, DetailView):
    template_name = 'todos/detail.html'
    slug_url_kwarg = 'detail_slug'
    context_object_name = 'task'


  

# Редактирование

class TaskUpdateView(LoginRequiredMixin, DataMixin, UpdateView):
    form_class = AddTaskForm
    template_name = 'todos/edit.html'
    slug_url_kwarg = 'edit_slug'
    
    def get_success_url(self):
        task = self.object 
        detail_slug = task.slug 
        return reverse('detail', kwargs={'detail_slug': detail_slug})

    def get_form_kwargs(self):
        kwargs = super(TaskUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user.id})
        return kwargs




# Успешное выполнение операции

def success(request):
    return render(request, 'todos/success.html')





# Авторизация\Регистрация

class SignUpUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'todos/register.html'
    success_url = reverse_lazy('sign_in')


class SignInUser(LoginView):
    form_class = LoginUserForm
    template_name = 'todos/login.html'
  

# Выход из учетной записи

def SignOutUser(request):
    logout(request)
    return redirect('home')




# Удаление задачи

class TaskDeleteView(LoginRequiredMixin, DataMixin, DeleteView):
    template_name = 'todos/delete.html'
    success_url = reverse_lazy('success')
    slug_url_kwarg = 'delete_slug'


# Удаление категории 

class CatChoiceView(LoginRequiredMixin, FormView):
    template_name = 'todos/choice.html'
    form_class = DeleteCategoryForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user.id})
        return kwargs

    def form_valid(self, form):
        cat = form.cleaned_data['choice_field']
        return HttpResponseRedirect(reverse_lazy('delete_cat', args=[cat.id]))


class CatDeleteView(LoginRequiredMixin, DataMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('success')
    template_name = 'todos/delete.html'


# Страница со статистикой профиля


@login_required
def profile_data(request):
    completed_tasks = Task.objects.filter(Q(completed=True) & Q(user=request.user)).count()
    uncompleted_tasks = Task.objects.filter(Q(completed=False) & Q(user=request.user)).count()
    date_joined = request.user.date_joined.date()
    categories = Category.objects.filter(user=request.user).count()
    context = {
        'completed': completed_tasks,
        'uncompleted': uncompleted_tasks,
        'date_joined': date_joined,
        'categories': categories,
        'cat': 0,
    }
    return render(request, 'todos/profile_data.html', context=context)


@login_required
def profile_change(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile_data')
    else:
        form = ProfileEditForm(instance=request.user)
    context = {
        'cat': 1,
        'form': form
    }
    return render(request, 'todos/profile_change.html', context=context)



# Удаление аккаунта

class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = get_user_model()
    template_name = 'todos/account_delete.html'
    success_url = reverse_lazy('home')
    extra_context = {'cat': 2}

    def get_object(self, queryset=None):
        return self.request.user
