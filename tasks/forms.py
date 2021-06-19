from django import forms
from django.db import models
from django.forms import widgets, DateTimeField
from .models import Task, Category


class TaskForm(forms.ModelForm):

    deadline = DateTimeField(
        input_formats=["%d/%m/%y %H:%M", "%d.%m.%Y %H:%M:%S"],
        widget=forms.widgets.DateTimeInput(
            attrs={"class": "form-control", "type": "datetime"},
        ),
        label='Крайний срок выполнения. Формат: «ДД/ММ/ГГ ЧЧ:ММ»',
        required=False,
    )

    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
        }

        labels = {
            "title": "Название задачи",
            "description": "Описание задачи",
            "deadline": "Крайний срок выполнения. Формат: ГГГГ-ММ-ДД ЧЧ:ММ",
            "category": "Категория",
            "completed": "Выполнено",
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("title",)

        widgets = {"title": forms.TextInput(attrs={"class": "form-control"})}

        labels = {"title": "Название категории"}
