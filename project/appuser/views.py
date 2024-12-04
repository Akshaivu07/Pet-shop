from django.shortcuts import render,redirect,get_object_or_404
from appadmin.models import CustomUser,Message,Donor_message,Admin_message
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random
from appdonor.models import Pet
from django.contrib.auth.hashers import make_password
import re
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from appuser.models import Cart,Adoption



# Create your views here.
def adoptor_reg(request):
    return render(request,'adoptor_registration.html')
def generate_otp_a():
    
    return ''.join(random.choices('0123456789', k=6))
def a_reg_db(request):
    if request.method == 'POST':
        firstname = request.POST['a_fname']
        lastname = request.POST['a_lname']
        email = request.POST['a_email']
        username = request.POST['a_username']
        address = request.POST['a_address']
        contact = request.POST['a_cnumber']
        usertype = request.POST['atext']
        otp = generate_otp_a()

        if len(contact) != 10 or not contact.isdigit():
            messages.error(request, 'Contact number must be 10 digits long and contain only numbers.')
            return redirect('donor_reg')

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            messages.error(request, 'Please enter a valid email address.')
            return redirect('donor_reg')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'This email address is already registered.')
            return redirect('donor_reg')

        if CustomUser.objects.filter(username=username).exists():
            messages.info(request, 'This username already exists.')
            return redirect('adoptor_reg')

        try:
            user = CustomUser.objects.create_user(first_name=firstname, last_name=lastname, email=email, address=address, contact=contact, user_type=usertype, username=username, password=otp)
            subject = "Your Password for signup"
            message = f"Your Password for signup is: {otp}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
            return redirect('login')
        except Exception as e:
            return render(request, 'home.html', {'message': f'Failed to send OTP: {e}'})

    return redirect('home')
def adoptor_home(request):
    user_id = request.user.id
    count = Message.objects.filter(user_id=user_id,visited=False).count()
    return render(request,'adoptor_home.html',{'count':count})
@login_required(login_url='home')
def view_approved(request):
    user_id = request.user.id
    count = Message.objects.filter(user_id=user_id,visited=False).count()
    approved_pets = Pet.objects.filter(approved=True)
    return render(request, 'user_pet_view.html', {'approved_pets': approved_pets,'count':count})
@login_required(login_url='home')
def pet_details(request,pet_id):
    
    pet = get_object_or_404(Pet, id=pet_id)
    return render(request, 'pet_details.html', {'pet': pet})
@login_required(login_url='home')
def adopt_details(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    donor = pet.donor  
    
    return render(request, 'adopt.html', {'pet': pet, 'donor': donor})

@login_required(login_url='home')
def confirm_adopt(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    adopter = request.user
    donor = pet.donor
    
    Cart.objects.create(
        user=adopter,
        pet_id=pet.id,
        pet_name=pet.pet_name,
        adoptor=adopter.get_full_name(),
        adoptor_email=adopter.email,  
        adoptor_contact=adopter.contact,  
        donor=donor.first_name,
        donor_email=donor.email,
        donor_contact=donor.contact,
        pet_breed=pet.pet_breed,
        pet_age=pet.pet_age,
        donor_id=pet.donor_id,
    )
    donor_message = Donor_message.objects.create(
        user=donor,
        message_doner=f'Your pet "{pet.pet_name}" has been adopted by {adopter.get_full_name()}.'
    )
    
    
    pet.delete()
    adopter_message = Message(user=adopter, message=f'You adopted the pet "{pet.pet_name}".')
    adopter_message.save()
    return redirect('view_approved')


def view_adopted_pets(request):
    user_id = request.user.id
    count = Message.objects.filter(user_id=user_id,visited=False).count()
    adopted_pets = Cart.objects.filter(user=request.user)
    return render(request, 'view_adopted_pets.html', {'adopted_pets': adopted_pets,'count':count})
def donor_notifi(request):
    user_id = request.user.id
    count = Donor_message.objects.filter(user_id=user_id, visited=False).count()
    donor_notifications = Donor_message.objects.filter(user=request.user,visited=False).order_by('-created_at')
    
    # Mark notifications as visited
    for notification in donor_notifications:
        notification.visited = True
        notification.save()
    
    return render(request, 'donor_notifi.html', {'donor_notifications': donor_notifications,'count':count})


@login_required(login_url='home')
def user_notification(request):
    user_id = request.user.id
    count = Message.objects.filter(user_id=user_id,visited=False).count()
    
    
    user_notifications = Message.objects.filter(user=request.user,visited=False).order_by('-created_at')
    for item in user_notifications:
        item.visited = True
        item.save()
    
    
    return render(request, 'user_notification.html', {'notifications': user_notifications,'count':count})
@login_required(login_url='home')
def admin_notification(request):
    
    carts = Cart.objects.all()
    for cart in carts:
        cart.visited2 = True
        cart.save()
    return render(request, 'admin_notification.html', {'carts': carts})

def u_password(request):
    user_id = request.user.id
    count = Message.objects.filter(user_id=user_id,visited=False).count()
    return render(request,'create_password.html',{'count':count})

def set_password(request):
    user_id = request.user.id
    count = Message.objects.filter(user_id=user_id,visited=False).count()
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if request.method == 'POST':
        email = request.POST.get('uemail')
        password = request.POST.get('upassword')
        confirm_password = request.POST.get('uconfirm_password')
        
        # Validate email format
        if not re.match(email_pattern, email):
            messages.error(request, 'Enter a valid email address.')
            return render(request, 'create_password.html', {'error': 'Enter a valid email address.'})
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'create_password.html', {'error': 'Passwords do not match.'})
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'create_password.html', {'error': 'Password must be at least 8 characters long.'})
        if not any(char.isdigit() for char in password):
            messages.error(request, 'Password must contain at least one digit.')
            return render(request, 'create_password.html', {'error': 'Password must contain at least one digit.'})
        if not any(char in "!@#$%^&*()_+-=[]{}|;:',.<>?/" for char in password):
            messages.error(request, 'Password must contain at least one special character.')
            return render(request, 'create_password.html', {'error': 'Password must contain at least one special character.'})
       
        hashed_password = make_password(password)
        
        user = CustomUser.objects.get(email=email)
        user.password = hashed_password
        user.save()
        return redirect('login')
    else:
        return render(request, 'create_password.html',{'count':count})
@login_required(login_url='home')
def adoptor_details(request, adoptor_id):
    adopter = get_object_or_404(CustomUser, id=adoptor_id, user_type=2)
    return render(request, 'adoptor_details.html', {'adopter': adopter})
def user_profile_view(request):
    user=request.user
    user_id = request.user.id
    count = Message.objects.filter(user_id=user_id,visited=False).count()
    
    return render(request, 'user_profile_view.html', {'user': user,'count':count})
def user_pro_edit(request, pk):
    user_id = request.user.id
    count = Message.objects.filter(user_id=user_id,visited=False).count()
    user = CustomUser.objects.get(id=pk)
    return render(request, 'user_profile_edit.html', {'user': user,'count':count})
def user_profile_edit(request, pk):
    user_id = request.user.id
    count = Message.objects.filter(user_id=user_id,visited=False).count()
    user = CustomUser.objects.get(id=pk)
    
    if request.method == 'POST':
        user.first_name = request.POST.get('u_fname')
        user.last_name = request.POST.get('u_lname')
        new_username = request.POST.get('u_username')
        user.username = new_username
        user.address = request.POST.get('u_address')
        user.contact = request.POST.get('u_cnumber')
        user.email = request.POST.get('u_email')
        
        
        if CustomUser.objects.exclude(id=pk).filter(username=new_username).exists():
            messages.error(request, 'This username is already taken. Please choose a different one.')
            return redirect('user_profile_edit', pk=pk)
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, user.email):
            messages.error(request, 'Please enter a valid email address.')
            return redirect('user_profile_edit', pk=pk)
        
        if CustomUser.objects.exclude(id=pk).filter(email=user.email).exists():
            messages.error(request, 'This email is already associated with another user.')
            return redirect('user_profile_edit', pk=pk)
        
        
        if CustomUser.objects.exclude(id=pk).filter(contact=user.contact).exists():
            messages.error(request, 'This contact number is already associated with another user.')
            return redirect('user_profile_edit', pk=pk)
        
        
        if len(user.contact) != 10 or not user.contact.isdigit():
            messages.error(request, 'Contact number must be 10 digits long and contain only numbers.')
            return redirect('user_profile_edit', pk=pk)
        
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('user_profile_view')
        
    return render(request, 'user_profile_edit.html',{'count':count})




