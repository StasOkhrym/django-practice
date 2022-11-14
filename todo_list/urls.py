from django.urls import path

from .views import (
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TagListView,
    TagDetailView,
    TagCreateView,
    TagUpdateView,
    TagDeleteView,
    toggle_task_state,
)

urlpatterns = [
    path("", TaskListView.as_view(), name="task-list"),
    path(
        "<int:pk>/change-state/",
        toggle_task_state,
        name="toggle-task-state",
    ),
    path("<int:pk>/detail", TaskDetailView.as_view(), name="task-detail"),
    path("<create/", TaskCreateView.as_view(), name="task-create"),
    path("<int:pk>/update", TaskUpdateView.as_view(), name="task-update"),
    path("<int:pk>/delete", TaskDeleteView.as_view(), name="task-delete"),
    path("tags/", TagListView.as_view(), name="tag-list"),
    path("tags/<int:pk>/", TagListView.as_view(), name="tag-detail"),
    path("tags/create/", TagCreateView.as_view(), name="tag-create"),
    path("tags/<int:pk/update/>", TagUpdateView.as_view(), name="tag-update"),
    path("tags/<int:pk/delete/>", TagDeleteView.as_view(), name="tag-delete"),
]

app_name = "todo_list"
