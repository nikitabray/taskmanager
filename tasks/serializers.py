from rest_framework import serializers
from rest_framework.exceptions import NotFound

from datetime import datetime

from .models import Category, Task


class CategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(allow_blank=True, allow_null=True)

    class Meta:
        model = Category
        fields = ["title"]


class CreateTaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer(allow_null=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "deadline",
            "completed",
            "category",
            "tags",
        ]

    def create(self, validated_data):
        category_title = validated_data["category"]["title"]
        if category_title:
            category = Category.objects.filter(title=category_title)
            if category:
                validated_data["category"] = category[0]
            else:
                raise NotFound(
                    f"There is no {category_title} category. You can create one."
                )
        else:
            validated_data["category"] = None
        return super().create(validated_data)


class DetailTaskSerializer(CreateTaskSerializer):
    created_at = serializers.DateTimeField("%d-%b-%Y %H:%M:%S")
    category_title = serializers.SerializerMethodField()
    completed = serializers.SerializerMethodField()
    deadline = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    category_slug = serializers.SerializerMethodField()
    modified_at = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = CreateTaskSerializer.Meta.fields + [
            "category_title",
            "category_slug",
            "modified_at",
        ]

    def get_completed(self, obj):
        return "Выполнена" if obj.completed else "Не выполнена"

    def get_description(self, obj):
        if obj.description:
            return obj.description
        else:
            return "Описание отсутствует"

    def get_category_title(self, obj):
        if obj.category:
            return obj.category.title
        else:
            return "Отсутствует"

    def get_deadline(self, obj):
        if obj.deadline:
            return datetime.strftime(obj.deadline, "%d-%b-%Y %H:%M")
        else:
            return "Отсутствует"

    def get_modified_at(self, obj):
        print(obj)
        if obj.modified_at:
            return datetime.strftime(obj.modified_at, "%d-%b-%Y %H:%M")
        else:
            return "Не было изменений"

    def get_category_slug(self, obj):
        if obj.category:
            return obj.category.slug
        else:
            return None


class ReadTasksDataSerializer(serializers.ModelSerializer):

    deadline = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "created_at",
            "modified_at",
            "deadline",
            "completed",
        ]

    def to_internal_value(self, data):
        if data.get("deadline") == "":
            data["deadline"] = None
        return super().to_internal_value(data)


class DumpTasksDataSerializer(serializers.ModelSerializer):

    category = serializers.CharField(allow_blank=True)
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ReadTasksDataSerializer.Meta.fields + ["tags", "category"]

    def get_tags(self, obj):
        if obj.tags:
            tags = ""
            for tag in obj.tags.all():
                tags += tag.name + ", "
            return tags
        else:
            return []
