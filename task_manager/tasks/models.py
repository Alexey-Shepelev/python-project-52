from django.db import models
from task_manager.users.models import LocalUser
from task_manager.statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=150, unique=True, null=False)
    description = models.TextField(blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, null=False)
    creator = models.ForeignKey(
        LocalUser,
        on_delete=models.PROTECT,
        related_name='creator'
    )
    executor = models.ForeignKey(
        LocalUser,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='executor'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'task'
        ordering = ['id']

    def __str__(self):
        return self.name
