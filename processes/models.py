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
        self.avg_rating = ((self.avg_rating * self.num_rates) + rate) /(self.num_rates + 1)
        return self.avg_rating
        

class Step(models.Model):
    order_number = models.IntegerField(default=1)
    step_name = models.CharField(max_length=100)
    description = models.TextField()
    process_id = models.ForeignKey(Process, on_delete=models.CASCADE , related_name='steps')
    
    def save(self,*args,**kwargs):  # this save method first automatically add a value for the order_number and then save it to db(because we only get data other than the order_number from the form)
                                    # this method will be called in the forms.py after the form check validations 
        if not self.order_number:
            lasts_step_obj = Step.objects.filter(process_id = self.process_id).order_by('-order_number').first()
            if lasts_step_obj:
                self.order_number = lasts_step_obj.order_number + 1
            else:
                self.order_number = 1
        super().save(*args, **kwargs)
        
    class Meta:
        ordering = ['order_number']