from django.views.generic import ListView
from .serializers import DetailTaskSerializer, CreateTaskSerializer
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from .models import Category, Task
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from .forms import TaskForm
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator


class CreateTask(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create-task.html'
    success_url = reverse_lazy('list of all tasks')


class UpdateTask(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create-task.html'
    success_url = reverse_lazy('list of all tasks')


def deleteTask(request, pk):
    task = Task.objects.get(pk=pk)
    context = {'item': task}

    if request.method == 'POST':
        task.delete()
        return redirect('/')
    return render(request, 'tasks/delete-task.html', context=context)


class AllTasksView(ListAPIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'tasks/index.html'

    def get(self, request, *args, **kwargs):
        data = Task.objects.all().select_related(
            'category').prefetch_related('tags').order_by('-id')
        ser = DetailTaskSerializer(data=data, many=True)
        ser.is_valid()
        p = Paginator(ser.data, 10)
        if 'page' in request.query_params:
            page = p.page(int(request.query_params['page']))
        else:
            page = p.page(1)
        
        context = {
            'data': page,
            'has_prev': page.has_previous,
            'has_next': page.has_next,
        }
        return Response(context)

class AllCategoriesView(ListView):
    template_name = 'tasks/categories.html'
    model = Category
