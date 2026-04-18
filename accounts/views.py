from django.shortcuts import render , redirect
from . models import CustomUser
from django.contrib.auth.hashers import make_password
import random, time
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
from .forms import RegistrationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login as auth_login

from django.contrib.auth import logout as auth_logout


def login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin/')
        else:
            role = request.user.role
            return redirect(f"{role}_dashboard")
    
    if request.method == 'POST':
        role = request.POST.get('role')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if role not in ["student", "teacher"]:
            messages.error(request, "Please select a role before logging in.")
            return render(request, 'accounts/login.html', {'username': username, 'role': role})

        user = authenticate(request, username=username, password=password)

        if user:
            if user.role != role:
                messages.error(request, "Role mismatch: you selected '%s' but your account is a %s." % (role, user.role))
                return render(request, 'accounts/login.html', {'username': username, 'role': role})

            if not user.is_active:
                messages.error(request, "Your account is not active. An admin must approve it before you can log in.")
                return render(request, 'accounts/login.html', {'username': username, 'role': role})

            auth_login(request, user)
            return redirect(f"{role}_dashboard")
        else:
            # authentication failed
            try:
                u = CustomUser.objects.get(username=username)
                if not u.is_active:
                    messages.error(request, "Your account exists but is not active. Please contact admin.")
                else:
                    messages.error(request, "Password incorrect for the given username.")
            except CustomUser.DoesNotExist:
                messages.error(request, "No account found with that username.")
            return render(request, 'accounts/login.html', {'username': username, 'role': role})

    return render(request, 'accounts/login.html')



def student_register(request):
    # unified registration for both roles
    if request.user.is_authenticated:
        return redirect(f"{request.user.role}_dashboard")

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            selected = form.cleaned_data.get('role')
            user.role = selected
            if selected == 'teacher':
                user.is_staff = True
                # make teachers active immediately instead of waiting for admin
                user.is_active = True
            else:
                user.is_staff = False
                user.is_active = True
            user.save()
            form.save_m2m()
            messages.success(request, "Account created. Please log in.")
            return redirect('login')
        else:
            messages.error(request, "There were errors in your submission. Please correct them below.")
    else:
        initial = {}
        # allow prefilling role via GET (used by teacher_register redirect)
        if request.GET.get('role'):
            initial['role'] = request.GET.get('role')
        form = RegistrationForm(initial=initial)
    return render(request, 'accounts/student_register.html', {'form': form})

# teacher_register kept for compatibility but now uses unified form

def teacher_register(request):
    # simply forward to the main registration view with the role pre‑selected
    if request.user.is_authenticated:
        return redirect(f"{request.user.role}_dashboard")

    if request.method == 'POST':
        # let student_register handle POST logic
        return student_register(request)
    # GET -> redirect with query parameter so the form picks up initial role
    from django.urls import reverse
    return redirect(reverse('student_register') + '?role=teacher')


def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)  # Properly logs out user and clears session
    return redirect('home')

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "No account found with this email.")
            return render(request, 'accounts/forgot_password.html')

        # Clear previous OTP session keys
        for key in ['reset_email', 'otp', 'otp_expiry', 'otp_verified']:
            request.session.pop(key, None)

        # Generate new OTP
        otp = random.randint(100000, 999999)
        request.session['reset_email'] = email
        request.session['otp'] = str(otp)
        request.session['otp_expiry'] = time.time() + 300  # 5 minutes validity

        # Send OTP via email
        send_mail(
            subject="Your Password Reset OTP.This message is from student management system",
            message=f"Your OTP is {otp}. It will expire in 5 minutes.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        messages.success(request, f"OTP sent to {email}. Please check your inbox.")
        return redirect('verify_otp')

    return render(request, 'accounts/forgot_password.html')


# Step 2: Verify OTP
def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        stored_otp = request.session.get("otp")
        expiry = request.session.get("otp_expiry")

        if not stored_otp or time.time() > expiry:
            messages.error(request, "OTP expired. Please request a new one.")
            return redirect('forgot_password')

        if entered_otp == stored_otp:
            request.session['otp_verified'] = True
            messages.success(request, "OTP verified! Now you can reset your password.")
            return redirect('reset_password')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'accounts/verify_otp.html')


# Step 3: Reset Password
def reset_password(request):
    if not request.session.get('otp_verified'):
        messages.error(request, "Unauthorized access.")
        return redirect('forgot_password')

    if request.method == "POST":
        password = request.POST.get("password")
        confirm = request.POST.get("confirm_password")

        if password != confirm:
            messages.error(request, "Passwords do not match.")
        else:
            email = request.session.get('reset_email')
            
            if not email:
                messages.error(request, "Session expired. Please start the reset process again.")
                return redirect('forgot_password')

            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                messages.error(request, "User not found for this email.")
                return redirect('forgot_password')


            user.password = make_password(password)
            user.save()

            # Clear OTP session keys
            for key in ['reset_email', 'otp', 'otp_verified', 'otp_expiry']:
                request.session.pop(key, None)

            messages.success(request, "Password reset successful! Please login.")
            return redirect('login')

    return render(request, 'accounts/reset_password.html')