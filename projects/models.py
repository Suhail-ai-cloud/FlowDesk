from django.db import models
from django.conf import settings
from accounts.models import Company

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="projects"
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects"
    )

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='ProjectMembership',
        related_name='projects'
    )

    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProjectMembership(models.Model):
    ROLE_CHOICES = (
        ('OWNER', 'Owner'),
        ('MEMBER', 'Member'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('user', 'project')  # 🔥 THIS LINE

