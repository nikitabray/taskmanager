from django.db import models
from slugify import slugify as py_slugify
from django.db.models.deletion import SET_NULL
from simple_history.models import HistoricalRecords
from taggit.managers import TaggableManager
from taggit.models import Tag, TaggedItem


class RuTag(Tag):
    class Meta:
        proxy = True

    def slugify(self, tag, i=None):
        return py_slugify(tag)
        return super().slugify(tag, i=i)


class RuTaggedItem(TaggedItem):
    class Meta:
        proxy = True

    @classmethod
    def tag_model(cls):
        return RuTag


class Category(models.Model):
    title = models.CharField(max_length=30, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=40)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def save(self, *args, **kwargs):
        self.slug = py_slugify(self.title)
        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(
        auto_now=True, 
        blank=True, 
        null=True
    )
    deadline = models.DateTimeField(
        blank=True,
        null=True,
    )
    completed = models.BooleanField(default=False)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=SET_NULL)
    tags = TaggableManager(
        through=RuTaggedItem, help_text="Список тэгов, разделенных запятыми", blank=True
    )
    history = HistoricalRecords()

    def save_without_historical_record(self, *args, **kwargs):
        self.skip_history_when_saving = True
        try:
            ret = self.save(*args, **kwargs)
        finally:
            del self.skip_history_when_saving
        return ret

    class Meta:
        verbose_name = ("Задача",)
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.title
