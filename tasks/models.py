from django.db import models
from django.db.models.deletion import SET_NULL
from simple_history.models import HistoricalRecords
from taggit.managers import TaggableManager


class Category(models.Model):
    title = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=40)

    class Meta:
        verbose_name = 'Category',
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


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
        null=True,
    )
    completed = models.BooleanField(
        default=False
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=SET_NULL
    )
    tags = TaggableManager(
        help_text='Список тегов, разделенных запятыми',
        blank=True
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Task',
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return self.title
