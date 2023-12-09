from django.db import models
from . extras import TimeStampedModel

__all__ = ['Department']

class Department(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    theme = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name