from django.urls import path
from .views import CreateCategory, HistoryView, TagView, deleteTask, CreateTask, UpdateTask, TasksView, CategoriesView

urlpatterns = [
    path("", TasksView.as_view(), name="list of all tasks"),
    path("create-task/", CreateTask.as_view(), name="create task"),
    path("update-task/<int:pk>/", UpdateTask.as_view(), name="update task"),
    path("delete-task/<int:pk>/", deleteTask, name="delete task"),
    path("categories/", CategoriesView.as_view(), name="list of categories"),
    path("create-category/", CreateCategory.as_view(), name="create category"),
    path("categories/<str:cat_slug>/", TasksView.as_view(), name="category related tasks"),
    path('tags/', TagView.as_view(), name="list of tags"), 
    path("tags/<str:tag_slug>/", TasksView.as_view(), name="tag related tasks"),
    path("history/<int:pk>/", HistoryView.as_view(), name="history of the task"),
]
