from django import forms
from .models import Task


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'deadline': forms.DateTimeInput(format='%d/%m/%Y %H:%M', attrs={'class': 'form-control', 'type': 'datetime'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }