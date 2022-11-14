from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from todo_list.forms import TaskSearchForm, TagSearchForm, TaskForm
from todo_list.models import Task, Tag


class TaskListView(generic.ListView):
    model = Task
    queryset = Task.objects.prefetch_related("tags")
    template_name = "todo_list/task_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)

        content = self.request.GET.get("content", "")
        not_completed = self.request.GET.get("not_completed", "")

        context["search_form"] = TaskSearchForm(
            initial={"content": content, "not_completed": not_completed}
        )
        return context

    def get_queryset(self):
        form = TaskSearchForm(self.request.GET)

        if form.is_valid():
            if form.cleaned_data["not_completed"]:
                return self.queryset.filter(
                    name__icontains=form.cleaned_data["content"], is_completed=False
                )
            return self.queryset.filter(content__icontains=form.cleaned_data["content"])


class TaskDetailView(generic.DetailView):
    model = Task


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("todo_list:task-list")


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy("todo_list:task-detail", args=[self.object.pk])


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("todo_list:task-list")


class TagListView(generic.ListView):
    model = Tag
    queryset = Tag.objects.all()
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TagSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        form = TagSearchForm(self.request.GET)

        if form.is_valid():
            if form.cleaned_data["name"]:
                return self.queryset.filter(name__icontains=form.cleaned_data["name"])
            return self.queryset


class TagDetailView(generic.DetailView):
    model = Tag
    fields = "__all__"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TagDetailView, self).get_context_data(**kwargs)

        tag = Tag.objects.get(id=self.kwargs["pk"])
        tasks = Task.objects.filter(tags__id=tag.id)
        context["tasks"] = tasks
        return context


class TagCreateView(generic.CreateView):
    model = Tag
    fields = "__all__"


class TagUpdateView(generic.UpdateView):
    model = Tag
    fields = "__all__"


class TagDeleteView(generic.DeleteView):
    model = Tag


def toggle_task_state(request, pk):
    task = Task.objects.get(id=pk)
    if not task.is_completed:
        task.is_completed = True
    else:
        task.is_completed = False
    task.save()
    return HttpResponseRedirect(reverse_lazy("todo_list:task-detail", args=[pk]))
