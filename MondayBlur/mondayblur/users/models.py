from django.db import models
from django.contrib.auth.models import User
from QnA.models import comment

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.png", upload_to="profile_pics")
    
    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
                                                                                                                                                                                                                                                                                           
#database for points
class Reward(models.Model): 
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    








        


