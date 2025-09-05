from django import forms
from django.forms import inlineformset_factory
from . models import Process, Step, AppComment

class ProcessForm(forms.ModelForm):
    class Meta:
        model = Process
        fields = ('title', 'description')

class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['step_name', 'description','order_number']
        widgets = {
            'order_number': forms.HiddenInput(),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['step_name'].widget.attrs['placeholder'] = 'Step name'
        self.fields['description'].widget.attrs['placeholder'] = 'Description'
        self.fields['order_number'].required = False   # 👈 make it optional(if it's required the formset.is_valid() will mark it invalid because it's empty when sent from the form in html-( we fill it with data inside our view after checking the form.is_valid() method ))


StepFormSet = inlineformset_factory(
    Process,
    Step,
    form=StepForm,
    extra=0,
    can_delete=True  # ✅ this enables deletion
)

class AppCommentForm(forms.ModelForm):
    class Meta:
        model = AppComment
        fields =['email','comment']
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        # Programmatically set placeholders for all other fields
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['comment'].widget.attrs['placeholder'] = 'Comment'