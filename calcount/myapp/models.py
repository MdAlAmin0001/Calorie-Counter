from django.db import models
from django.contrib.auth.models import User


class user_profile(models.Model):
    GENDER=[
        ('Male','male'),
        ('Female','female'),
    ]
    profile_pic=models.ImageField(upload_to='media/profile pic', null=True, blank=True)
    name=models.CharField(max_length=100, null=True, blank=True)
    age=models.FloatField()
    gender=models.CharField(max_length=100, choices=GENDER,null=True, blank=True)
    height=models.FloatField()
    weight=models.FloatField()
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.name
    
    
class ConsumedCalories(models.Model):
    user = models.ForeignKey(user_profile, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255, null=True, blank=True)
    calories_consumed = models.PositiveIntegerField( null=True, blank=True)
    date_consumed = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.item_name} - {self.date_consumed}'
    
