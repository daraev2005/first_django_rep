from django.urls import path
from . import views


urlpatterns = [
    path('', views.PreviewContactView.as_view(), name='preview' ),
    path('todo_list/', views.TaskListView.as_view(), name='home'),
    path('sign_up/', views.SignUpUser.as_view(), name='sign_up'),
    path('sign_in/', views.SignInUser.as_view(), name='sign_in'),
    path('sign_out/', views.SignOutUser, name='sign_out'), 
    path('update/<int:todo_id>/', views.CompletedView.as_view(), name='update'),
    path('detail/<slug:detail_slug>/', views.TaskDetailView.as_view(), name='detail'),
    path('delete/<slug:delete_slug>/', views.TaskDeleteView.as_view(), name='delete'),
    path('add/', views.AddTaskView.as_view(), name='add_task'),
    path('add_cat/', views.AddCatView.as_view(), name='add_cat'),
    path('predelete_cat/', views.CatChoiceView.as_view(), name='predelete_cat'),
    path('delete_cat/<int:pk>', views.CatDeleteView.as_view(), name='delete_cat'),
    path('edit/<slug:edit_slug>/', views.TaskUpdateView.as_view(), name='edit'), 
    path('success/', views.success, name='success'),
    path('profile_data/', views.profile_data, name='profile_data'),
    path('profile_change/', views.profile_change, name='profile_change'),
    path('profile_delete/', views.AccountDeleteView.as_view(), name='profile_delete')
]