from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    
    #auto_now gives us a date last modified
    date_modified = models.DateTimeField(User, auto_now= True)
    def __str__(self):
        return self.user.username

#Create profile when new user signs up
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwards):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        #Have the user follow themselves
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

#This does the same task as reciever noted above function
#post_save.connect(create_profile,sender=User)