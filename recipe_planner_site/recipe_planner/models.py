from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Recipe(models.Model):
    """
    Represents a recipe entry associated with a user.

    Fields:
        user (ForeignKey): Optional reference to the user who created the recipe.
        day (CharField): The day the recipe is intended for (e.g., "Monday").
        name (CharField): The name/title of the recipe.
        description (CharField): A short description of the recipe.
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    day = models.CharField(max_length=100, default='something')
    name = models.CharField(max_length=100, default='something')
    description = models.CharField(max_length=100, default='something')

