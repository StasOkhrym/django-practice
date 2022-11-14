from django.db.models.functions import datetime
from django.test import TestCase
from django.urls import reverse
from unittest import mock

from todo_list.models import Task, Tag


class TagTests(TestCase):
    def test_create_tag(self):
        form_data = {"name": "test"}
        response = self.client.post(
            reverse("todo_list:tag-create"), data=form_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Tag.objects.get(id=1).name, "test")

    def test_update_tag(self):
        tag = Tag.objects.create(name="test")
        form_data = {"name": "new_test"}

        response = self.client.post(
            reverse("todo_list:tag-update", args=[1]), data=form_data
        )
        tag.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(tag.name, "new_test")

    def test_delete_tag(self):
        Tag.objects.create(name="test")

        response = self.client.post(
            reverse("todo_list:tag-delete", args=[1])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Tag.objects.filter(id=1).exists())

    def test_search_tag(self):
        Tag.objects.create(name="test")
        Tag.objects.create(name="name")
        Tag.objects.create(name="super_name")
        response = self.client.get(
            reverse("todo_list:tag-list") + "?name=me"
        )
        tags = Tag.objects.filter(name__icontains="me")

        self.assertEqual(
            list(response.context["tag_list"]),
            list(tags)
        )
        self.assertEqual(Tag.objects.count(), 3)
        self.assertEqual(len(tags), 2)


class TaskTests(TestCase):
    def setUp(self) -> None:
        self.tag = Tag.objects.create(name="test")

    def test_delete_task(self):
        Task.objects.create(
            content="TaskTest",
            is_completed=False,
            deadline=datetime.datetime.now(),
        )

        response = self.client.post(
            reverse("todo_list:task-delete", args=[1])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=1).exists())

    def test_search_task(self):
        Task.objects.create(
            content="TaskTest",
            is_completed=False,
            deadline=datetime.datetime.now(),
        )
        Task.objects.create(
            content="TestName",
            is_completed=False,
            deadline=datetime.datetime.now(),
        )
        Task.objects.create(
            content="SuperName",
            is_completed=False,
            deadline=datetime.datetime.now(),
        )
        response = self.client.get(
            reverse("todo_list:task-list") + "?content=me"
        )
        tasks = Task.objects.filter(content__icontains="me")

        self.assertEqual(
            list(response.context["task_list"]),
            list(tasks)
        )
        self.assertEqual(Task.objects.count(), 3)
        self.assertEqual(len(tasks), 2)
