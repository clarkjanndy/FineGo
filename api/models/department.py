from django.db import models
from . extras import TimeStampedModel

__all__ = ['Department']

class Department(TimeStampedModel):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=2)
    description = models.TextField(null=True, blank=True)
    theme = models.CharField(max_length=255, default='#4e73df')

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        self.abbreviation = self.abbreviation.upper()
        return super().save(*args, **kwargs)

    @property
    def card_style(self):
        return f'style="height: 150px; background-color: {self.theme}"'
    