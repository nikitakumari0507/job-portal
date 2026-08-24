from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    USER_TYPES = (

        ('candidate', 'Candidate'),

        ('employer', 'Employer'),

    )

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPES
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )
    
    resume = models.FileField(
    upload_to="resumes/",
    blank=True,
    null=True
)

    def __str__(self):
        return self.username