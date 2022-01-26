from django.contrib.auth.models import AbstractUser
from django.db import models
# here we combine features from different apps,
# The code we write here is very specific to this project
# this is essentially the core of the project

# the core app is not a reusable app


class User(AbstractUser):
    email = models.EmailField(unique=True)
