from django.db.models.functions import datetime
from django.test import TestCase

from todo_list.models import Task, Tag


class ModelTests(TestCase):
    def test_tag_str(self):
        name = "TestName"
        tag = Tag.objects.create(name=name)

        self.assertEqual(str(tag), name)

    def test_task_str(self):
        task = Task.objects.create(
            content="tests",
            is_completed=False,
            deadline=datetime.datetime.now(),
        )

        self.assertEqual(str(task), "tests")
