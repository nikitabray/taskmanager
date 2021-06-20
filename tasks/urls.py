from django.urls import path
from .views import (
    CreateCategory,
    HistoryView,
    TagView,
    CreateTask,
    UpdateTask,
    TasksView,
    CategoriesView,
    deleteAllCategories,
    deleteAllTags,
    deleteAllTasks,
    deleteTask,
    dumpToCSV,
    generateData,
    loadFromCSV,
)

urlpatterns = [
    path("", TasksView.as_view(), name="list of all tasks"),
    path("create-task/", CreateTask.as_view(), name="create task"),
    path("update-task/<int:pk>/", UpdateTask.as_view(), name="update task"),
    path("delete-task/<int:pk>/", deleteTask, name="delete task"),
    path("categories/", CategoriesView.as_view(), name="list of categories"),
    path("create-category/", CreateCategory.as_view(), name="create category"),
    path(
        "categories/<str:cat_slug>/", TasksView.as_view(), name="category related tasks"
    ),
    path("tags/", TagView.as_view(), name="list of tags"),
    path("tags/<str:tag_slug>/", TasksView.as_view(), name="tag related tasks"),
    path("history/<int:pk>/", HistoryView.as_view(), name="history of the task"),
    path("delete-all-tasks", deleteAllTasks, name="delete all tasks"),
    path("delete-all-categories", deleteAllCategories, name="delete all categories"),
    path("delete-all-tags", deleteAllTags, name="delete all tags"),
    path("generate-data", generateData, name="generate data"),
    path("save-to-csv", dumpToCSV, name="save to csv"),
    path("load-from-csv", loadFromCSV, name="load from csv"),
]
