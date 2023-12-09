from django.db import models
from . extras import TimeStampedModel

__all__ = ['SystemInformation']

class SystemInformation(TimeStampedModel):
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self) -> str:
        return self.title