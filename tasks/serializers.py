from rest_framework import serializers
from rest_framework.exceptions import NotFound
from .models import Category, Task
from datetime import datetime
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer


class CategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(allow_blank=True)

    class Meta:
        model = Category
        fields = ['title']


class CreateTaskSerializer(serializers.ModelSerializer):
    deadline = serializers.DateTimeField(
        "%d-%m-%Y %H:%M", allow_null=True, required=False)
    category = CategorySerializer(allow_null=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'created_at',
            'deadline', 'completed', 'category',
            'tags'
        ]

    def create(self, validated_data):
        category_title = validated_data['category']['title']
        if category_title:
            category = Category.objects.filter(title=category_title)
            if category:
                validated_data['category'] = category[0]
            else:
                raise NotFound(
                    f'There is no {category_title} category. You can create one.')
        else:
            validated_data['category'] = None
        return super().create(validated_data)


class DetailTaskSerializer(CreateTaskSerializer):
    created_at = serializers.DateTimeField("%d-%b-%Y %H:%M:%S")
    category_title = serializers.SerializerMethodField()
    tags = TagListSerializerField()
    completed = serializers.SerializerMethodField()
    deadline = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = CreateTaskSerializer.Meta.fields + ['category_title']
    
    def get_completed(self, obj):
        return 'Выполнена' if obj.completed else 'Не выполнена'

    def get_description(self, obj):
        if obj.description:
            return obj.description
        else:
            return 'Описание отсутствует'

    def get_category_title(self, obj):
        if obj.category:
            return obj.category.title
        else:
            return 'Отсутствует'
    

    def get_deadline(self, obj):
        if obj.deadline:
            return datetime.strftime(obj.deadline, '%d-%b-%Y %H:%M')
        else:
            return 'Отсутствует'
    
