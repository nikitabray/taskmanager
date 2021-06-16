from django.db import models
from django.db.models.deletion import SET_DEFAULT
from simple_history.models import HistoricalRecords

class Tag(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Tag',
        verbose_name_plural = 'Tags'


class Category(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Category',
        verbose_name_plural = 'Categories'


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    deadline = models.DateTimeField(
        blank=True,
        null=True
    )
    completed = models.BooleanField(
        default=False
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        default='No category',
        on_delete=models.SET_DEFAULT
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Task',
        verbose_name_plural = 'Tasks'

    
  
  
# Create your models here.
