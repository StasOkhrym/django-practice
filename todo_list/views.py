from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from todo_list.forms import TaskSearchForm
from todo_list.models import Task


class TaskListView(generic.ListView):
    model = Task
    queryset = Task.objects.select_related("tags")
    template_name = "todo_list/task_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")
        not_completed = self.request.GET.get("not_completed", "")

        context["search_form"] = TaskSearchForm(
            initial={"name": name, "not_completed": not_completed}
        )
        return context

    def get_queryset(self):
        form = TaskSearchForm(self.request.GET)

        if form.is_valid():
            if form.cleaned_data["name"]:
                return self.queryset.filter(
                    content__icontains=form.cleaned_data["name"]
                )
            return self.queryset


def toggle_task_state(request, pk):
    task = Task.objects.get(id=pk)
    if not task.is_completed:
        task.is_completed = True
    else:
        task.is_completed = False
    task.save()
    return HttpResponseRedirect(reverse_lazy("todo_list:task-list", args=[pk]))


