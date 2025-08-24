from . models import Process, Step
from django import forms

class ProcessForm(forms.ModelForm):
    
    class Meta:
        model = Process
        fields = ('title','description')

# class StepFormSet(forms.ModelForm):
    
#     class Meta:
#         model = Step
#         fields = ('step_name','description')
        
from django.forms import inlineformset_factory

StepFormSet = inlineformset_factory(
    Process, Step,
    fields=('step_name', 'description'),
    extra=1,  # just one empty form to start
    can_delete=True
)