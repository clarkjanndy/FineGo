from django.db import models
from . extras import TimeStampedModel

__all__ = ['FAQ']

class FAQ(TimeStampedModel):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self) -> str:
        return self.question

   