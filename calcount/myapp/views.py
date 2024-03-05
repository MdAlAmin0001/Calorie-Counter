from django.shortcuts import get_object_or_404, render,redirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from .forms import *
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model
from myapp.tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib import messages
from django.core.mail import EmailMessage
from p.settings import EMAIL_HOST_USER
import random
from django.core.mail import send_mail



def userprofile_update(request):
    profile_user=0
    try:
        profile_user=user_profile.objects.get(user=request.user)
    except:
        pass
    if request.method == 'POST' and profile_user:
        form = userprofile_form(request.POST, request.FILES, instance=profile_user)
        if form.is_valid():
            form.save()
            return redirect('home')
    elif request.method== 'POST':
        form = userprofile_form(request.POST)
        if form.is_valid():
            co=form.save(commit=False)
            co.user=request.user
            co.save()
            return redirect('home')
    elif profile_user:
        form=userprofile_form(instance=profile_user)
    else:
        form=userprofile_form()
    
    return render(request, 'userprofile.html',{'form':form})



def activate(request,uid64,token):
    User=get_user_model()
    try:
        uid= force_str(urlsafe_base64_decode(uid64))
        user=User.objects.get(pk=uid)

    except:
        user =None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active=True
        user.save()
        return redirect('register')

    print("account activation: ", account_activation_token.check_token(user, token))

    return redirect('loginpage')


def activateEmail(request,user,to_mail):
    mail_sub='Active your user Account'
    message=render_to_string("template_activate.html",{
        'user': user.username,
        'domain':get_current_site(request).domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user),
        'protocol':'https' if request.is_secure() else 'http'
    })
    email= EmailMessage(mail_sub, message, to=[to_mail])
    if email.send():
        messages.success(request,f'Dear')
    else:
        message.error(request,f'not')


def register(request):
    if request.method == 'POST':
        form = register_form(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('loginpage')
    else:
        form = register_form()
    return render(request, 'register.html', {'form': form})



def loginpage(request):
    if request.method == 'POST':
        form=login_form(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(request, username=username,password=password)
            if user:
                login(request,user)
                return redirect('home')
    else:
        form=login_form()
    return render(request, 'loginpage.html',{'form':form})

def logoutpage(request):
    logout(request)
    return redirect('loginpage')






def home(request):
    try:
        user_profile_instance = user_profile.objects.get(user=request.user)
    except user_profile.DoesNotExist:
        
        return redirect('userprofile_update')

    if user_profile_instance.gender == 'male':
        bmr = 66.47 + (13.75 * user_profile_instance.weight) + (5.003 * user_profile_instance.height) - (6.755 * user_profile_instance.age)
    else:
        bmr = 655.1 + (9.563 * user_profile_instance.weight) + (1.850 * user_profile_instance.height) - (4.676 * user_profile_instance.age)

    required_calories = bmr

    form = DailyConsumedCaloriesForm()

    if request.method == 'POST':
        form = DailyConsumedCaloriesForm(request.POST)
        if form.is_valid():
            consumed_calories = form.save(commit=False)
            consumed_calories.user = user_profile_instance
            consumed_calories.save()
            messages.success(request, 'Consumed calories added successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Error adding consumed calories. Please check the form.')

    consumed_calories_list = ConsumedCalories.objects.filter(user=user_profile_instance)
    
    sum_calories = sum(i.calories_consumed for i in consumed_calories_list)
    need = required_calories - sum_calories
        
    context = {
        'user_profile': user_profile_instance,
        'required_calories': required_calories,
        'consumed_calories_list': consumed_calories_list,
        'form': form,
        'sum': sum_calories,
        'need': need,
    }

    return render(request, 'home.html', context)

def update_consumed_items(request,id):
    item=get_object_or_404(ConsumedCalories, id=id)
    if request.method == 'POST':
        form=DailyConsumedCaloriesForm(request.POST,  instance=item)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DailyConsumedCaloriesForm(instance=item)
    return render(request,'update_item.html', {'form':form})

def delete_item(request, id):
    item = get_object_or_404(ConsumedCalories, pk=id)
    item.delete()
    return redirect('home')


def forgetpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            otp = random.randint(111111, 999999)
            user.otp_token = otp
            user.save()

            
            subject = f"Important: Your One-Time Password {otp}"

            msg = f"""
            Dear {user.username} ,

            We received a request to verify your identity.
            Your one-time password is: {otp}

            Please enter this code to complete your request.

            For your security:

            * Never share your OTP with anyone.
            * This code is valid only for [2 minutes].
            * Delete this email once you've used the OTP.

            If you didn't request this OTP, please contact us immediately

            Sincerely,

            The Developer Team
            """
            from_mail = EMAIL_HOST_USER
            recipient = [email]
            send_mail(
                subject=subject,
                recipient_list=recipient,
                from_email=from_mail,
                message=msg,
            )
            return render(request, 'changepassword.html', {'email': email})
        except User.DoesNotExist:
            # Email not found in the database
            message = "Email address not found. Please check and try again."
            return render(request, 'forgetpassword.html', {'error_message': message})
    else:
        return render(request, 'forgetpassword.html')


def changepassword(request):
    if request.method == "POST":
        mail = request.POST.get('email')
        otp = request.POST.get('otp')
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')
        user = User.objects.get(email = mail)
        if user.otp_token != otp:
            return redirect('forgetpassword')
        if password != c_password:
            return redirect('forgetpassword')
        user.set_password(password)
        
        user.save()
        return redirect('loginpage')
    return render(request, 'changepassword.html')
    