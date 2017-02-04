from django.db import models
from django.contrib.auth.models import AbstractUser

# The models for the Account application


## Model for Fomo's Users
class FomoUser(AbstractUser):

	###The fields commented below are inherited from the AbstractBaseUsser and AbstractUser classes

    # username
    # first_name
    # last_name
    # password
    # email
    # last_login

    #Gender Types

    GENDER_CHOICES = (
    	('male', 'Male'),
    	('female', 'Female'),
    	('other', 'Other'),
    )
        
    birth_date = models.DateTimeField('Birth Date')
    gender = models.TextField(null=True, blank=True, choices=GENDER_CHOICES, default = 'other',)


