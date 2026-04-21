from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    TYPE_CHOICES = [
        ("task", "Task"),
        ("note", "Note"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    item_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default="task")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="low")
    due_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title