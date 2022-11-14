from django.db.models.functions import datetime
from django.test import TestCase
from django.urls import reverse

from todo_list.models import Task, Tag


class PublicTests(TestCase):
    def setUp(self) -> None:
        Tag.objects.create(name="Test")
        Tag.objects.create(name="NewTag")
        Tag.objects.create(name="TestTag")
        Task.objects.create(
            content="TestName",
            is_completed=False,
            deadline=datetime.datetime.now(),
        )
        Task.objects.create(
            content="TaskTest",
            is_completed=False,
            deadline=datetime.datetime.now(),
        )

    def test_task_list(self):
        response = self.client.get(reverse("todo_list:task-list"))
        tasks = Task.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["task_list"]),
            list(tasks),
        )
        self.assertTemplateUsed(response, "todo_list/task_list.html")

    def test_task_detail(self):
        response = self.client.get(reverse("todo_list:task-detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo_list/task_detail.html")

    def test_tag_list(self):
        response = self.client.get(reverse("todo_list:tag-list"))
        tasks = Tag.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["tag_list"]),
            list(tasks),
        )
        self.assertTemplateUsed(response, "todo_list/tag_list.html")

    def test_tag_detail(self):
        response = self.client.get(reverse("todo_list:tag-detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todo_list/tag_detail.html")

    def test_toggle_task_state(self):
        task = Task.objects.get(id=1)
        response_add = self.client.post(
            reverse("todo_list:toggle-task-state", kwargs={"pk": task.id})
        )
        task.refresh_from_db()
        self.assertEqual(response_add.status_code, 302)
        self.assertEqual(task.is_completed, True)

        response_remove = self.client.post(
            reverse("todo_list:toggle-task-state", kwargs={"pk": task.id})
        )
        task.refresh_from_db()
        self.assertEqual(response_remove.status_code, 302)
        self.assertEqual(task.is_completed, False)

