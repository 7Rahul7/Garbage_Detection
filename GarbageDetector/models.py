from django.db import models
from django.contrib.auth.models import User

# Create your models here

class Upload(models.Model):
    file = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name



class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tokens = models.IntegerField(default=1000) # this is the bonus 1000 coins when signup 
    
    def __str__(self):
        return f"{self.user.username} Profile"

