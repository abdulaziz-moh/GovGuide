from django.shortcuts import render, redirect
from . forms import SignupForm, UserProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def signup_veiw(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('/processes/process_list/')
        return render(request, 'accounts/signup.html', {'form':form})
    else:
        form = SignupForm()
        return render(request, 'accounts/signup.html', {'form':form})
        
        
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/processes/process_list/')            
            
        return render(request, 'accounts/login.html', {'form':form})
    else:
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form':form})
    
    
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile') # Redirect to the user's profile page
        else:
            return render(request, 'accounts/profile.html',{'user':user,'form': form})
    else:
        form = UserProfileForm(instance=request.user) # instance=request.user will make it update instead of creating new
        return render(request, 'accounts/profile.html',{'user':user,'form':form})

@login_required
def delete_account(request):
    user = request.user
    user.delete()
    logout(request)
    return redirect('process_list')
