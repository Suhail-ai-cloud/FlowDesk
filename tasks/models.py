from django.db import models
from django.conf import settings
from projects.models import Project


class Task(models.Model):
    PRIORITY = (('LOW','Low'),('MEDIUM','Medium'),('HIGH','High'))
    STATUS = (('PENDING','Pending'),('IN_PROGRESS','In Progress'),('COMPLETED','Completed'))

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY)
    status = models.CharField(max_length=20, choices=STATUS, default='PENDING')
    assigned_to = models.ManyToManyField(
    settings.AUTH_USER_MODEL,
    related_name="assigned_tasks",
    blank=True
)

    created_at = models.DateTimeField(auto_now_add=True)

    def is_overdue(self):
        from django.utils.timezone import now
        return self.due_date < now().date() and self.status != 'COMPLETED'


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Attachment(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="attachments"
    )
    file = models.FileField(upload_to="task_attachments/")
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name