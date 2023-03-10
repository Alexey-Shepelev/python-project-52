from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'status'
        ordering = ['id']

    def __str__(self):
        return self.name
