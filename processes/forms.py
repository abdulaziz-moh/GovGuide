from . models import Process, Step
from django import forms
from django.forms import inlineformset_factory

class ProcessForm(forms.ModelForm):
    
    class Meta:
        model = Process
        fields = ('title','description')

class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['step_name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add placeholders
        self.fields['step_name'].widget.attrs['placeholder'] = 'Step name'
        self.fields['description'].widget.attrs['placeholder'] = 'Description'


StepFormSet = inlineformset_factory(
    Process,
    Step,
    form=StepForm,   # 👈 use custom form here
    extra=1,
    can_delete=True
)