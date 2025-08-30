from django.db import models
from django.contrib.auth.models import User
from processes.models import Process

# Create your models here.
class Review(models.Model):
    rating = models.FloatField()
    comment = models.TextField()
    rated_at = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name="review")
    process_id = models.ForeignKey(Process, on_delete=models.CASCADE,related_name="review")