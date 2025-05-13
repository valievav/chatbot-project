from django.db import models


class Recipe(models.Model):
    """
    Recipe model
    """
    name = models.CharField(max_length=255)
    steps = models.TextField()
    favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
