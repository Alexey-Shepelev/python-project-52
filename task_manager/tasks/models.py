from django.db import models
from task_manager.users.models import LocalUser
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        null=False,
        verbose_name=_('Name')
    )
    description = models.TextField(blank=True, verbose_name=_('Description'))
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        null=False,
        verbose_name=_('Status')
    )
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
        related_name='executor',
        verbose_name=_('Executor')
    )
    labels = models.ManyToManyField(
        Label,
        blank=True,
        related_name='label',
        verbose_name=_('Labels'),
        through='TaskLabelRelation',
        # through_fields=('task', 'label')
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'task'
        ordering = ['id']

    def get_labels(self):
        return ", ".join([label.name for label in self.labels.all()])

    def __str__(self):
        return self.name


class TaskLabelRelation(models.Model):
    """Intermediate model for many-to-many relations between tasks and labels.
    Needed to restrict deletion of labels used by tasks."""
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
