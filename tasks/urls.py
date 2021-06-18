from django.urls import path
from .views import AllTasksView, AllCategoriesView, deleteTask, CreateTask, UpdateTask

urlpatterns = [
    path('', AllTasksView.as_view(), name='list of all tasks'),
    path('create-task/', CreateTask.as_view(), name='create task'),
    path('update-task/<int:pk>', UpdateTask.as_view(), name='update task'),
    path('delete-task/<int:pk>', deleteTask, name='delete task'),
    path('categories', AllCategoriesView.as_view(), name='categories')
]
