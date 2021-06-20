from collections import OrderedDict
import csv
import re
import random
import string

from lorem_text import lorem

from .models import Task, Category
from .serializers import DumpTasksDataSerializer, ReadTasksDataSerializer

class TaskManager:
    @classmethod
    def create_from_data(cls, data: dict, category: str, tags: str):
        ser = ReadTasksDataSerializer(data=data)
        ser.is_valid(raise_exception=True)
        if not ser.validated_data:
            return None
        instance = ser.create(ser.validated_data)
        instance = cls.add_category_to_task(instance, category)
        instance = cls.add_tags_to_task(instance, tags)
        return instance

    @classmethod
    def add_category_to_task(self, task_instance, category_title: str):
        if not category_title:
            return task_instance

        category = Category.objects.filter(title=category_title)
        if category:
            task_instance.category = category[0]
        else:
            Category(title=category_title).save()
            task_instance.category = Category.objects.get(title=category_title)
        return task_instance

    @classmethod
    def add_tags_to_task(self, task_instance, tags: str):
        if not tags:
            return task_instance

        pattern = r"([^,]*)"
        p = re.compile(pattern)
        s = p.findall(tags)
        tags = []
        for match in s:
            if match and match not in [" " * x for x in range(3)]:
                tags.append(match.strip())
        task_instance.tags.add(*tags)
        return task_instance


class DumpData:
    def get_data(self, qs=None, *args, **kwargs) -> OrderedDict:
        if not qs:
            qs = Task.objects.all()
        ser = DumpTasksDataSerializer(instance=qs, many=True)
        return ser.data

    def save_to_csv(self, filename: str) -> bool:
        if not filename.endswith(".csv"):
            filename += ".csv"
        with open(f"./csv/{filename}", "w", newline="") as csvfile:
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

    def load_from_csv(self, read_obj) -> bool:
        csv_reader = csv.DictReader(read_obj)
        for row in csv_reader:
            category = row["category"]
            tags = row["tags"]
            TaskManager.create_from_data(
                row, category, tags
            ).save_without_historical_record()
        return True


class DataGenerator:
    @classmethod
    def get_random_string(
        cls, chars=string.ascii_letters + string.digits, size=10
    ) -> str:
        return "".join(random.choice(chars) for _ in range(size))

    @classmethod
    def generate_title(cls) -> str:
        return lorem.words(random.randint(1, 5))

    @classmethod
    def generate_description(cls) -> str:
        description = ""
        if random.randint(0, 1):
            description = lorem.paragraph()
        return description

    @classmethod
    def generate_deadline(cls) -> str:
        deadline = ""
        if random.randint(0, 1):
            d, m, y = (
                str(random.randint(1, 28)),
                str(random.randint(1, 12)),
                str(random.randint(21, 22)),
            )
            hour, minute = str(random.randint(0, 23)), str(random.randint(0, 59))
            deadline = f"20{y}-{m}-{d} {hour}:{minute}:00"
        return deadline

    @classmethod
    def generate_completed(cls) -> bool:
        return random.choice([True, False])

    @classmethod
    def generate_tags(cls, list_size=10) -> str:
        tags = []
        for _ in range(list_size):
            title_len = random.randint(3, 10)
            tags.append(
                "tag_"
                + cls.get_random_string(chars=string.ascii_lowercase, size=title_len)
            )
        return tags

    @classmethod
    def generate_categories(cls, list_size=10) -> list:
        list_of_categories = []
        chars = string.ascii_uppercase
        for _ in range(list_size):
            title_len = random.randint(1, 12)
            list_of_categories.append(
                "category_" + cls.get_random_string(chars=chars, size=title_len)
            )
        return list_of_categories + [""]

    @classmethod
    def generate_task_data(cls) -> str:

        data = {
            "title": cls.generate_title(),
            "description": cls.generate_description(),
            "deadline": cls.generate_deadline(),
            "completed": cls.generate_completed(),
        }

        return data

    @classmethod
    def generate(cls, count=100) -> None:
        list_of_categories = cls.generate_categories(max(1, int(count / 10)))
        list_of_tags = cls.generate_tags(max(3, int(count / 4)))
        for _ in range(count):
            data = cls.generate_task_data()
            tags = (
                ", ".join(
                    [
                        random.choice(list_of_tags)
                        for _ in range(random.randint(0, 7))
                    ]
                )
                + ", "
            )
            category = random.choice(list_of_categories)
            obj = TaskManager.create_from_data(data, category, tags)
            if obj:
                obj.save_without_historical_record()
                print(f"Создана задача с именем {obj}")
