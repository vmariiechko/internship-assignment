from django.db import models
from django.contrib.auth.models import User


class SMS(models.Model):
    """
    The model represents SMS messages with its author and number of views.
    """

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=160)
    views_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'SMSes'
