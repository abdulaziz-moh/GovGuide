from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label=False,
        widget=forms.EmailInput(attrs={'placeholder':'Email'})
        )
    
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','password1','password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        # Programmatically set placeholders for all other fields
        self.fields['first_name'].widget.attrs['placeholder'] = 'Firstname'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Lastname'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password1'].widget.attrs['placeholder'] = 'New Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        
        # Hide the labels for these fields
        self.fields['first_name'].label = False
        self.fields['last_name'].label = False
        self.fields['username'].label = False
        self.fields['password1'].label = False
        self.fields['password2'].label = False