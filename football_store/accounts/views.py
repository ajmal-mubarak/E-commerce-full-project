import random
from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from orders.models import UserAddress
from .models import EmailOTP
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


# =========================
# ACCOUNT PAGE
# =========================
def accounts(request):
    return render(request, "account.html")


# =========================
# REGISTER WITH EMAIL OTP
# =========================
@never_cache
def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, "register.html", {"username": username, "email": email})

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, "register.html", {"email": email})

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return render(request, "register.html", {"username": username})

        EmailOTP.objects.filter(email=email, is_verified=False).delete()

        otp = str(random.randint(100000, 999999))

        EmailOTP.objects.create(
            username=username,
            email=email,
            password=password,
            otp=otp
        )

        request.session["email"] = email

        send_mail(
            "Football Shop OTP Verification",
            f"Hello {username},\n\nYour OTP is {otp}.\nIt is valid for 5 minutes.",
            "mubarakajmal0@gmail.com",
            [email],
            fail_silently=False,
        )

        return redirect("verify_otp")

    return render(request, "register.html")


# =========================
# VERIFY OTP
# =========================
@never_cache
def verify_otp(request):
    email = request.session.get("email")
    if not email:
        return redirect("register")

    otp_record = EmailOTP.objects.filter(email=email, is_verified=False).last()
    if not otp_record:
        messages.error(request, "OTP not found. Please register again.")
        return redirect("register")

    if request.method == "POST":
        otp_input = request.POST.get("otp")

        if otp_record.is_expired():
            messages.error(request, "OTP expired. Please resend.")
            return redirect("verify_otp")

        if otp_input != otp_record.otp:
            messages.error(request, "Invalid OTP.")
            return redirect("verify_otp")

        user = User.objects.create_user(
            username=otp_record.username,
            email=otp_record.email,
            password=otp_record.password
        )

        otp_record.is_verified = True
        otp_record.save()

        login(request, user)
        messages.success(request, "Registration successful!")
        return redirect("index")

    return render(request, "verify_otp.html", {"email": email})


# =========================
# RESEND OTP
# =========================
@never_cache
def resend_otp(request):
    if request.method != "POST":
        return JsonResponse({"success": False})

    email = request.session.get("email")
    if not email:
        return JsonResponse({"success": False, "message": "Session expired"})

    old = EmailOTP.objects.filter(email=email, is_verified=False).last()
    if not old:
        return JsonResponse({"success": False, "message": "No OTP found"})

    EmailOTP.objects.filter(email=email, is_verified=False).delete()

    otp = str(random.randint(100000, 999999))
    new_otp = EmailOTP.objects.create(
        username=old.username,
        email=email,
        password=old.password,
        otp=otp
    )

    send_mail(
        "New Football Shop OTP",
        f"Hello {new_otp.username},\n\nYour new OTP is {otp}.\nValid for 5 minutes.",
        "mubarakajmal0@gmail.com",
        [email],
        fail_silently=False,
    )

    return JsonResponse({"success": True, "message": "OTP resent"})


# =========================
# LOGIN
# =========================
@never_cache
def login_user(request):
    # Show message if redirected from protected page
    if 'next' in request.GET:
        messages.info(request, "Please login to continue")
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}! 👋")
            # Redirect to next page if available
            next_url = request.GET.get('next', 'index')
            return redirect(next_url)

        messages.error(request, "Invalid username or password")

    return render(request, "account.html")


# =========================
# LOGOUT
# =========================
@never_cache
def logout_user(request):
    logout(request)
    return redirect("index")


# =========================
# PROFILE + CHANGE PASSWORD
# =========================
@login_required
def profile_page(request):
    addresses = UserAddress.objects.filter(user=request.user)
    address_types = ["home", "work"]

    if request.method == "POST":

        # CHANGE PASSWORD (NO OTP)
        if "change_password" in request.POST:
            current_password = request.POST.get("current_password")
            new_password = request.POST.get("new_password")
            confirm_new_password = request.POST.get("confirm_new_password")

            if not request.user.check_password(current_password):
                messages.error(request, "Current password incorrect")
                return redirect("profile")

            if new_password != confirm_new_password:
                messages.error(request, "New passwords do not match")
                return redirect("profile")

            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)

            messages.success(request, "Password updated successfully")
            return redirect("profile")

        # UPDATE PROFILE
        if "update_profile" in request.POST:
            username = request.POST.get("username")
            email = request.POST.get("email")

            if User.objects.filter(username=username).exclude(id=request.user.id).exists():
                messages.error(request, "Username already taken")
                return redirect("profile")

            request.user.username = username
            request.user.email = email
            request.user.save()

            messages.success(request, "Profile updated")
            return redirect("profile")

        # SAVE ADDRESS
        if "save_address" in request.POST:
            address_type = request.POST.get("address_type")

            address, _ = UserAddress.objects.get_or_create(
                user=request.user,
                address_type=address_type
            )

            address.full_name = request.POST.get("full_name")
            address.phone = request.POST.get("phone")
            address.address = request.POST.get("address")
            address.city = request.POST.get("city")
            address.pincode = request.POST.get("pincode")
            address.save()

            messages.success(request, "Address saved")
            return redirect("profile")

    return render(request, "profile.html", {
        "addresses": addresses,
        "address_types": address_types,
    })



@never_cache
def forgot_password(request):

    useremail = User.objects.filter(email=request.POST.get("email")).first()

    if request.method == "POST":
        email = request.POST.get("email")

        user = User.objects.filter(email=email).first()
        if not user:
            messages.error(request, "No account found with this email.")
            return redirect("forgot_password")

        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = request.build_absolute_uri(
            f"/accounts/reset-password/{uid}/{token}/"
        )

        send_mail(
            "Reset your Football Shop password",
            f"Hi {user.username},\n\nClick the link below to reset your password:\n{reset_link}\n\nIf you didn’t request this, ignore this email.",
            "mubarakajmal0@gmail.com",
            [email],
            fail_silently=False,
        )

        messages.success(request, "Password reset link sent to your email.")
        return redirect("login")

    return render(request, "forgot_password.html", {'useremail': useremail})

@never_cache
def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if not user:
        messages.error(request, "Invalid reset link.")
        return redirect("login")

    token_generator = PasswordResetTokenGenerator()
    if not token_generator.check_token(user, token):
        messages.error(request, "Reset link expired or invalid.")
        return redirect("login")

    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "reset_password.html")

        try:
            validate_password(password, user)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return render(request, "reset_password.html")

        user.set_password(password)
        user.save()   # 🔥 THIS LINE WAS MISSING OR NOT HIT BEFORE

        messages.success(request, "Password reset successful. Please login.")
        return redirect("login")

    return render(request, "reset_password.html")