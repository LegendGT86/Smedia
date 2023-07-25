from django.db import models
from django.contrib.auth.models import User

#creating A User Profile Model
#This will associate one user to one profile, on delete all fields cascaded below will be deleted
#one profile can follow many, symettrical in that you can follow them, they dont have to follow you back
#Blank true meaning if you decide, you dont have to follow anyone
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self",
                                     related_name="followed_by",
                                     symmetrical=False,
                                     blank=True)

