from django.shortcuts import render,redirect
from vendor.forms import VendorForm
from .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages,auth
from .utils import detectUser,send_verification_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserForm  # Import your UserForm class
from .utils import send_verification_mail  # Import your mail sending function

from vendor.models import Vendor
from orders.models import Order
from django.template.defaultfilters import slugify

import datetime
# Restrict the Vendor from customer page

def check_role_vendor(user):
    if user.role==1:
        return True
    else:
        raise PermissionDenied

# Restrict the customer  from Vendor page

def check_role_customer(user):
    if user.role==2:
        return True
    else:
        raise PermissionDenied


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    
    # In the context of web forms, 
    # POST requests are used when submitting data to the server, such as when a user submits a form.
    elif request.method == 'POST':
        # request.POST prints the contents of the request.POST dictionary to the console.
        # form = UserForm(request.POST), it creates an instance of the UserForm using the data from request.POST
        # This condition checks if the submitted form data is valid according to the rules defined in the UserForm class.
       
        form = UserForm(request.POST)
        if form.is_valid():
            # the form is ready to save, this is not yet save.
            # After we submit the form the data with fields is stored in the cleaned_data dictionary.
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            user.set_password(password)
            user.save()
            
            # Send verification mail to user.
            
            email_template ='accounts/emails/account_verification.html'
            mail_subject   = 'Please activate your account.'
            send_verification_mail(request,user, email_template, mail_subject)
            messages.success(request, 'Your account has been registered successfully!')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid Form. Please correct the errors.')
            return render(request, 'accounts/registerUser.html', {'form': form})

    else:
        # When a user first visits and enters the webpage URL, the form will display on the webpage (i.e., GET request).
        # calling the Userform class 
        form = UserForm()
        return render(request, 'accounts/registerUser.html', {'form': form, 'messages': messages.get_messages(request)})

    # Add a default return statement at the end of the view
    return HttpResponse("Internal Server Error")  # Import HttpResponse if not already imported



def registerVendor(request):
    userform = UserForm()
    v_form  = VendorForm()
    context = {
            'form'  : userform,
            'v_form': v_form,
           }
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in!')
        return redirect('myAccount')
    
    elif request.method=='POST':
        # store the data and create user
        
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST,request.FILES)
       
        if form.is_valid() and v_form.is_valid():
         
            first_name = form.cleaned_data['first_name']
            last_name  = form.cleaned_data['last_name']
            email      = form.cleaned_data['email']
            username   = form.cleaned_data['username']
            password   = form.cleaned_data['password']
            user       =  User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor_name = v_form.cleaned_data['vendor_name']
            vendor.vendor_slug = slugify(vendor_name) + '-'+ str(user.id)
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
      
            vendor.save()
            
            # Send verification mail to user.
            
            email_template ='accounts/emails/account_verification.html'
            mail_subject   = 'Please activate your account.'
            try:
            
                send_verification_mail(request,user,email_template,mail_subject)
                messages.success(request,"Your account has been registered sucessfully! Please wait for the approval.")
            except:
     
                return redirect('registerVendor')
        else:
        
            messages.error(request, 'Invalid Form. Please correct the errors.')
            return render(request, 'accounts/registerUser.html', {'form': form})

    else:
        '''userform = UserForm()
        v_form  = VendorForm()
        context = {
            'form'  : userform,
            'v_form': v_form,
           }'''
        pass
    return render(request,'accounts/registerVendor.html',context)


def activate(request,uidb64,token):

# Activate the user by setting the is_active to True.
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,OverflowError,ValueError,User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'Congratulations! your account is activated.')
        return redirect('myAccount')
    else:

        messages.error(request,'Invalid activatation link')
        return redirect('myAccount')
        
           
def login(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in!')
        return redirect('myAccount')
        
        
    elif request.method =="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email,password=password)
        
        if user is not None and user.is_active:
            auth.login(request,user)
            messages.success(request, 'You are logged in.')
            return redirect('myAccount')
        else:
            messages.error(request,'Invalid log in credentials')
            return redirect('login')
            
    return render(request,'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request,'You are logged out.')
    return redirect('login')


# When you logged into the account then only you have access to the myaccount dashboard.

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirecturl = detectUser(user)
    return redirect(redirecturl)

@login_required(login_url='login')   
@user_passes_test(check_role_customer)
def custDashboard(request):
    orders  = Order.objects.filter(user=request.user,is_ordered=True)
    recent_orders = orders[:5]
    context  = {
        'orders' : orders, 
        'orders_count' : orders.count(),   
        'recent_orders' : recent_orders,   
    }
    return render (request,'accounts/custDashboard.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    vendor = Vendor.objects.get(user = request.user)
    orders = Order.objects.filter(vendors__in = [vendor.id],is_ordered = True).order_by('-created_at')
   
    recent_orders  = orders[:5]
    
    # current month revenue.
    
    current_month        = datetime.datetime.now().month
    current_month_orders = Order.objects.filter(vendors__in = [vendor.id],created_at__month = current_month)
    
    current_month_revenue = 0
    for i in current_month_orders:
        current_month_revenue +=  i.get_total_by_vendor()['grand_total']
    
        
    
    # Total revenue.
    total_revenue  = 0
    for i in orders:
        total_revenue += i.get_total_by_vendor()['grand_total']
        
    
    context = {
        'vendor':vendor,
        'orders' : orders,
        'orders_count' : orders.count(),
        'recent_orders' : recent_orders ,
        'total_revenue'  : total_revenue,
        'current_month_revenue' : current_month_revenue,
    }
  
    return render (request,'accounts/vendorDashboard.html',context)


def forgot_password(request):
    if request.method =='POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            
            # send reset password email.
            mail_subject = 'Reset your password.'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_mail(request,user,email_template,mail_subject)
            messages.success(request,'Password reset link has been sent to your email address!.')
            return redirect('login')
        else:
            send_verification_mail(request,user)
            messages.error(request,'Account does not exist.')
            return redirect('forgot_password')
            
    return render(request,'accounts/forgot_password.html')

def reset_password_validate(request,uidb64,token):
    # Validate the user by decoding token and user pk.
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,OverflowError,ValueError,User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
       request.session['uid'] = uid 
       messages.info(request,'Please Reset your password.')
        
       return redirect('reset_password')
    else:

        messages.error(request,'This link has been expired!')
        return redirect('myAccount')
    
    
def reset_password(request):
    if request.method=='POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request,"Password  reset sucussfull!")
            return redirect('login')
        else:
            messages.error(request,'Password do not match!')
            return redirect('reset_password')
            
    return render(request,'accounts/reset_password.html')



    
    
       
    
    
    
        