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


class PredictionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='history/')
    predicted_label = models.CharField(max_length=100)
    recyclable_status = models.CharField(max_length=20)  # "Recyclable" or "Non-Recyclable"
    predicted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.predicted_label} - {self.predicted_at.strftime('%Y-%m-%d %H:%M')}"