from django.db import models
from django.utils import timezone
from datetime import timedelta
from users.models import User

class Weather(models.Model):
    users =models.ForeignKey(User,on_delete=models.CASCADE) 
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    description = models.CharField(max_length=250)
    humidity = models.IntegerField()
    pressure = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def delete_old_data(cls):
        """Delete records older than 5 minutes"""
        time_limit = timezone.now() - timedelta(minutes=5)
        cls.objects.filter(created_at__lt=time_limit).delete()

    def __str__(self):
        return f"{self.city} - {self.temperature}°C"
