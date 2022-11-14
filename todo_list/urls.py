from django.urls import path

from .views import (
    TaskListView,
    toggle_task_state,
)

urlpatterns = [
    path("", TaskListView.as_view(), name="task-list"),
    path(
        "<int:pk>/change-state/",
        toggle_task_state,
        name="toggle-task-state",
    ),
]

app_name = "todo_list"
