from django.db.models.signals import post_save
from django.dispatch import receiver
from tasks.models import Task, Comment
from .models import ActivityLog, Notification
from django.contrib.auth import get_user_model
from .middleware import get_current_user
from django.contrib.auth.models import AnonymousUser


User = get_user_model()

@receiver(post_save, sender=Task)
def log_task_activity(sender, instance, created, **kwargs):

    actor = get_current_user()

    if not actor or isinstance(actor, AnonymousUser):
        return  # ❗ stop here safely

    if created:
        ActivityLog.objects.create(task=instance, user=actor, action="Task created")
    else:
        if instance.status == 'COMPLETED':
            ActivityLog.objects.create(task=instance, user=actor, action="Task completed")
        else:
            ActivityLog.objects.create(task=instance, user=actor, action="Task updated")

@receiver(post_save, sender=Comment)
def log_comment_activity(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            task=instance.task,
            user=instance.user,
            action="Comment added"
        )

        # 🔥 Notify ALL assigned users except commenter
        for user in instance.task.assigned_to.all():
            if user != instance.user:
                Notification.objects.create(
                    user=user,
                    message=f"New comment on task: {instance.task.title}"
                )
@receiver(post_save, sender=Comment)
def log_comment_activity(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            task=instance.task,
            user=instance.user,
            action="Comment added"
        )

        for user in instance.task.assigned_to.all():
            if user != instance.user:
                Notification.objects.create(
                    user=user,
                    message=f"New comment on task: {instance.task.title}"
                )
