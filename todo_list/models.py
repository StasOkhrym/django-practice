from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    is_completed = models.BooleanField()
    tags = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.content
