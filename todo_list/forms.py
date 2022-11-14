from django import forms

from todo_list.models import Task, Tag


class TaskSearchForm(forms.Form):
    content = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by content"}),
    )
    not_completed = forms.BooleanField(required=False)


class TagSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )


class TaskForm(forms.ModelForm):
    deadline = forms.SplitDateTimeField()
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple, required=False
    )

    class Meta:
        model = Task
        fields = "__all__"
