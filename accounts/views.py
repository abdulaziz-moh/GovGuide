from django.shortcuts import render, redirect
from . forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout 
from django.contrib import messages

# Create your views here.

def signup_veiw(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('processes/process-list')
        pass
    else:
        form = SignupForm()
        return render(request, 'accounts/signup.html', {'form':form})
        
        
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            return render(request, 'processes/process-list')
            
        pass
    else:
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form':form})
    
    

def logout_view(request):
    logout(request)
    return redirect('login')     