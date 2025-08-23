from . models import Process, Step
from django import forms

class ProcessForm(forms.ModelForm):
    
    class Meta:
        model = Process
        fields = ('title','description')

class StepFormSet(forms.ModelForm):
    
    class Meta:
        model = Step
        fields = ('step_name','description')