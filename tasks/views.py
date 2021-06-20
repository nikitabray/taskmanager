from tasks.utils import DataGenerator, DumpData
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.http import FileResponse

from taggit.models import Tag

from .models import Category, Task
from .forms import CategoryForm, GenerateForm, LoadFromCSV, SaveToCSV, TaskForm
from .serializers import DetailTaskSerializer



class CreateTask(CreateView):
    # Create an object of the Task model
    model = Task
    form_class = TaskForm
    template_name = "tasks/create-task.html"
    success_url = reverse_lazy("list of all tasks")


class UpdateTask(UpdateView):
    # Update task
    model = Task
    form_class = TaskForm
    template_name = "tasks/create-task.html"
    success_url = reverse_lazy("list of all tasks")


def deleteTask(request, pk):
    # Delete task
    task = Task.objects.get(pk=pk)
    context = {"item": task}

    if request.method == "POST":
        task.delete()
        return redirect("/")
    return render(request, "tasks/delete-task.html", context=context)


def deleteAllTasks(request):
    if request.method == "POST":
        for task in Task.objects.all():
            task.delete()
        return redirect("/")
    return render(request, "tasks/delete-all-tasks.html")


def deleteAllCategories(request):
    if request.method == "POST":
        for category in Category.objects.all():
            category.delete()
        return redirect("/")
    return render(request, "tasks/delete-all-categories.html")


def deleteAllTags(request):
    if request.method == "POST":
        for category in Tag.objects.all():
            category.delete()
        return redirect("/")
    return render(request, "tasks/delete-all-tags.html")


def generateData(request):
    if request.method == "POST":
        count = int(request.POST.get("count"))
        DataGenerator.generate(count)
        return redirect("/")

    form = GenerateForm
    context = {"form": form}
    return render(request, "tasks/generate-data.html", context=context)


def dumpToCSV(request):
    if request.method == "POST":
        filename = request.POST.get("filename")
        if not filename.endswith(".csv"):
            filename += ".csv"
        DumpData().save_to_csv(filename)
        response = FileResponse(open(f"./csv/{filename}", "rb"), as_attachment=True)
        return response

    form = SaveToCSV
    context = {"form": form}
    return render(request, "tasks/save-to-csv.html", context=context)


def loadFromCSV(request):
    if request.method == "POST":
        form = LoadFromCSV(request.POST, request.FILES)
        if form.is_valid():
            decoded_file = request.FILES["file"].read().decode("utf-8").splitlines()
            DumpData().load_from_csv(decoded_file)
            return redirect("/")
    else:
        form = LoadFromCSV
    return render(request, "tasks/load-from-csv.html", {"form": form})


class TasksView(ListAPIView):

    # Custom GET function used because of conflicts between TemplateHTMLRenderer and ListAPIView
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tasks/tasks.html"

    def get(self, request, cat_slug=None, tag_slug=None, *args, **kwargs):
        # Get queryset of tasks by category slug
        if cat_slug:
            data = (
                Task.objects.filter(category__slug=cat_slug)
                .select_related("category")
                .prefetch_related("tags")
                .order_by("-modified_at")
            )
        # Get queryset of tasks by tag slug
        elif tag_slug:
            data = (
                Task.objects.filter(tags__slug=tag_slug)
                .select_related("category")
                .prefetch_related("tags")
                .order_by("-modified_at")
            )
        # Get queryset of all tasks
        else:
            data = (
                Task.objects.all()
                .select_related("category")
                .prefetch_related("tags")
                .order_by("-modified_at")
            )
        ser = DetailTaskSerializer(data=data, many=True)
        ser.is_valid()
        p = Paginator(ser.data, 10)
        if "page" in request.query_params:
            page = p.page(int(request.query_params["page"]))
        else:
            page = p.page(1)

        context = {
            "data": page,
            "has_prev": page.has_previous,
            "has_next": page.has_next,
        }
        return Response(context)


class CreateCategory(CreateView):
    # Create an object of the Category model
    model = Category
    form_class = CategoryForm
    template_name = "tasks/create-category.html"
    success_url = reverse_lazy("list of categories")


class CategoriesView(ListView):
    # Get list of categories
    template_name = "tasks/categories.html"
    model = Category
    queryset = Category.objects.all().order_by("title")


class TagView(ListView):
    # Get list of tags
    template_name = "tasks/tags.html"
    model = Tag
    queryset = Tag.objects.all().order_by("name")


class HistoryView(ListAPIView):
    # Get Task object history
    template_name = "tasks/history.html"
    renderer_classes = [TemplateHTMLRenderer]
    model = Task

    def get(self, request, pk, *args, **kwargs):
        data = Task.objects.get(pk=pk).history.all()
        ser = DetailTaskSerializer(data=data, many=True)
        ser.is_valid()
        return Response({"data": ser.data})
