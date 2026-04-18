from django.shortcuts import redirect , render 
from django.contrib import messages
from accounts.models import CustomUser
# Create your views here.
from .models import ContactMessage
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import update_session_auth_hash

def home(request):
    return render(request, "Homepage/home_page.html")
    

def about(request):
    return render(request , 'Homepage/about.html')


def contact(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject="None",
            message=message
        )
        return render(request, 'Homepage/contact.html', {'success': True})

    return render(request, 'Homepage/contact.html')


def change_pass(request):
    if not request.user.is_authenticated:
        return redirect('login')  # user not logged in

    username = request.user.username
    role = request.user.role

    if request.method == 'POST':
        old_password = request.POST.get('old-password')
        new_password = request.POST.get('new-password')
        confirm_password = request.POST.get('confirm-password')
        

        # Set new password
        user = CustomUser.objects.get(username=username)
        if not check_password(old_password , user.password):
            messages.error(request, "❌ Old password is incorrect ❌")
            return redirect('change_pass')
        
        if old_password == new_password:
            messages.error(request, "❌Old password & new password are same.❌")
            return redirect('change_pass')

        # Check new passwords match
        if new_password != confirm_password:
            messages.error(request, "❌ New passwords do not match ❌")
            return redirect('change_pass')

        user.password = make_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        
        messages.success(request, "Password changed successfully.")
        return redirect(f"{role}_dashboard")
        
        
    return render(request, 'Homepage/change_pass.html')