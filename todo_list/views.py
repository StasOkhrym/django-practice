from django.views import generic

from todo_list.forms import TaskSearchForm
from todo_list.models import Task


class TaskListView(generic.ListView):
    model = Task
    queryset = Task.objects.select_related("tags_id")
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



