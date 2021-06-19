import csv
from .models import Task, Category
from collections import OrderedDict
from .serializers import DumpTasksDataSerializer, ReadTasksDataSerializer
import re
import random
import string


class DumpData:
    def get_data(self, qs=None, *args, **kwargs) -> OrderedDict:
        if not qs:
            qs = Task.objects.all()
        ser = DumpTasksDataSerializer(instance=qs, many=True)
        return ser.data

    def save_to_csv(self) -> bool:
        with open("tasks.csv", "w", newline="") as csvfile:
            fieldnames = [
                "title",
                "description",
                "created_at",
                "modified_at",
                "deadline",
                "completed",
                "category",
                "tags",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            data = self.get_data()
            for task in data:
                writer.writerow(
                    {
                        "title": task["title"],
                        "description": task["description"],
                        "created_at": task["created_at"],
                        "modified_at": task["modified_at"],
                        "deadline": task["deadline"],
                        "completed": task["completed"],
                        "category": task["category"],
                        "tags": task["tags"],
                    }
                )

    def load_from_csv(self):
        with open("tasks.csv", "r") as read_obj:
            csv_reader = csv.DictReader(read_obj)
            for row in csv_reader:
                ser = ReadTasksDataSerializer(data=row)
                ser.is_valid()
                instance = ser.create(ser.validated_data)
                tags = self.get_tags(row["tags"])
                instance.tags.add(*tags)
                if row["category"]:
                    return self.add_category_to_task(instance, row["category"])
                else:
                    return instance.save()
        return "Success"

    def add_category_to_task(self, task_instance, category_title: str):
        category = Category.objects.filter(title=category_title)
        if category:
            task_instance.category = category[0]
        else:
            Category(title=category_title).save()
            task_instance.category = Category.objects.get(title=category_title)
        task_instance.save()

    def get_tags(self, tags: str) -> list:
        pattern = r"([^,]*)"
        p = re.compile(pattern)
        s = p.findall(tags)
        res = []
        for match in s:
            if match and match != ' ':
                res.append(match.strip())
        return res


class DataGenerator:

    @classmethod
    def get_random_string(cls, chars = string.ascii_letters + string.digits, size=10):
        
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(size))

    @classmethod
    def generate_categories(cls, array_size=12):
        pass

