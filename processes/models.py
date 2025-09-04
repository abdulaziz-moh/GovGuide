from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Process(models.Model):
    title = models.CharField(max_length=200 )
    description = models.TextField()
    num_rates = models.IntegerField(default=0)  # updated from the reviews class
    avg_rating = models.FloatField(default=0.0)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE, related_name='processes') # we may delete a post if the user is deleted( on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    def average_rating(self,rate):   # will be used in reviws app
        new_num_rates = self.num_rates + 1
        new_avg_rating = ((self.avg_rating * self.num_rates) + rate) / new_num_rates
        
        # Update the object's attributes in memory
        self.num_rates = new_num_rates
        self.avg_rating = new_avg_rating
        
        # Save the changes to the database
        self.save()  # 👈 This is the crucial missing part
        
        return self.avg_rating
        

class Step(models.Model):
    order_number = models.IntegerField(default=1)
    step_name = models.CharField(max_length=100)
    description = models.TextField()
    process_id = models.ForeignKey(Process, on_delete=models.CASCADE , related_name='steps')
    
    class Meta:
        ordering = ['order_number']
        
class AppComment(models.Model):
    email = models.EmailField()
    comment = models.TextField()