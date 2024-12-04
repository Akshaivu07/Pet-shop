from django.shortcuts import render,redirect,get_object_or_404
from appadmin.models import CustomUser,Category,Donation_message,Donor_message
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random
from appdonor.models import Pet
from django.contrib.auth.hashers import make_password
import re
from django.contrib.auth.decorators import login_required
from appuser.models import Cart




# Create your views here.
def donor_reg(request):
    return render(request,'donor_registration.html')
def generate_otp():
    
    return ''.join(random.choices('0123456789', k=6))
def d_reg_db(request):
    if request.method == 'POST':
        firstname = request.POST['d_fname']
        lastname = request.POST['d_lname']
        email = request.POST['d_email']
        username = request.POST['d_username']
        address = request.POST['d_address']
        contact = request.POST['d_cnumber']
        usertype = request.POST['dtext']
        otp = generate_otp()

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
            return redirect('donor_reg')

        try:
            user = CustomUser.objects.create_user(first_name=firstname, last_name=lastname, email=email, address=address, contact=contact, user_type=usertype, username=username, password=otp)
            subject = "Your Password for signup"
            message = f"Your password for signup is: {otp}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
            return redirect('login')
        except Exception as e:
            return render(request, 'home.html', {'message': f'Failed to send OTP: {e}'})

    return redirect('home')
def edit_donor_pro(request, pk):
    user_id = request.user.id
    count = Donor_message.objects.filter(user_id=user_id,visited=False).count()
    user = CustomUser.objects.get(id=pk)
    return render(request, 'edit_donor_profile.html', {'user': user,'count':count})

def edit_donor_profile(request, pk):
    user_id = request.user.id
    count = Donor_message.objects.filter(user_id=user_id,visited=False).count()
    user = CustomUser.objects.get(id=pk)
    
    if request.method == 'POST':
        user.first_name = request.POST.get('d_fname')
        user.last_name = request.POST.get('d_lname')
        new_username = request.POST.get('d_username')
        user.username = new_username
        user.address = request.POST.get('d_address')
        user.contact = request.POST.get('d_cnumber')
        user.email = request.POST.get('d_email')
        
        
        if CustomUser.objects.exclude(id=pk).filter(username=new_username).exists():
            messages.error(request, 'This username is already taken. Please choose a different one.')
            return redirect('edit_donor_profile', pk=pk)
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, user.email):
            messages.error(request, 'Please enter a valid email address.')
            return redirect('edit_donor_profile', pk=pk)
        
        if CustomUser.objects.exclude(id=pk).filter(email=user.email).exists():
            messages.error(request, 'This email is already associated with another user.')
            return redirect('edit_donor_profile', pk=pk)
        
        # Check if the contact number already exists
        if CustomUser.objects.exclude(id=pk).filter(contact=user.contact).exists():
            messages.error(request, 'This contact number is already associated with another user.')
            return redirect('edit_donor_profile', pk=pk)
        
        if len(user.contact) != 10 or not user.contact.isdigit():
            messages.error(request, 'Contact number must be 10 digits long and contain only numbers.')
            return redirect('edit_donor_profile', pk=pk)
        
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('view_donor_profile')
        
    return render(request, 'edit_donor_profile.html',{'count':count})

    

def view_donor_profile(request):
    user_id = request.user.id
    count = Donor_message.objects.filter(user_id=user_id,visited=False).count()
    user=request.user
    
    return render(request, 'view_donor_profile.html', {'user': user,'count':count})




       
@login_required(login_url='home')       
def donor_home(request):
    user_id = request.user.id
    count = Donor_message.objects.filter(user_id=user_id,visited=False).count()
    
    
   
    return render(request, 'donor_home.html', {'count': count})

    
@login_required(login_url='home')
def donor_form(request):
    user_id = request.user.id
    count = Donor_message.objects.filter(user_id=user_id,visited=False).count()
    category=Category.objects.all()
    return render(request,'donation_form.html',{'cat':category,'count':count})
@login_required(login_url='home')
def pet_db(request):
    user_id = request.user.id
    count = Donor_message.objects.filter(user_id=user_id,visited=False).count()
    if request.method == 'POST':
        pet_name = request.POST.get('pname')
        pet_breed = request.POST.get('pbreed')
        pet_age = request.POST.get('page')
        pet_image = request.FILES.get('file')
        description = request.POST.get('description')  # Get description field from the form
        select = request.POST.get('sel_cat')
        
        # Check if any field is empty
        if not all([pet_name, pet_breed, pet_age, pet_image, select]):
            messages.error(request, 'Please fill out all fields.')
            return redirect('donor_form')
        
        pet_category = Category.objects.get(id=select)
        pet = Pet(
            pet_name=pet_name,
            pet_breed=pet_breed,
            pet_age=pet_age,
            pet_image=pet_image,
            cat=pet_category,
            donor=request.user,
            description=description  # Save description to the Pet instance
        )
        pet.save()
        
        # Construct the donation message with the donor's name
        message_text = f"A pet named: {pet.pet_name} is added to the adoption"
        
        # Create the donation message
        donation_message = Donation_message(donate=message_text, user=request.user)
        
        # Save the donation message
        donation_message.save()

        # Display success message
        messages.success(request, 'Successfully added to the donation page.')
        
        # Redirect to donor_form
        return redirect('donor_form')
    
    # Render the donation form if the request method is not POST
    return render(request, 'donation_form.html',{'count':count})


@login_required(login_url='home')
def show_donation_messages(request):
    pets = Pet.objects.select_related('donor').all()

    
    for pet in pets:
        pet.visited = True
        pet.save()

    return render(request, 'donation_messages.html', {'pets': pets})

    

@login_required(login_url='home')
def d_password(request):
    user_id = request.user.id
    count = Donor_message.objects.filter(user_id=user_id,visited=False).count()
    return render(request,'create_password_d.html',{'count':count})
@login_required(login_url='home')
def set_password_d(request):
    user_id = request.user.id
    count = Donor_message.objects.filter(user_id=user_id, visited=False).count()
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if request.method == 'POST':
        email = request.POST.get('demail')
        password = request.POST.get('dpassword')
        confirm_password = request.POST.get('dconfirm_password')
        
        # Validate email format
        if not re.match(email_pattern, email):
            messages.error(request, 'Enter a valid email address.')
            return render(request, 'create_password_d.html', {'error': 'Enter a valid email address.'})
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'create_password_d.html', {'error': 'Passwords do not match.'})
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'create_password_d.html', {'error': 'Password must be at least 8 characters long.'})
        if not any(char.isdigit() for char in password):
            messages.error(request, 'Password must contain at least one digit.')
            return render(request, 'create_password_d.html', {'error': 'Password must contain at least one digit.'})
        if not any(char in "!@#$%^&*()_+-=[]{}|;:',.<>?/" for char in password):
            messages.error(request, 'Password must contain at least one special character.')
            return render(request, 'create_password_d.html', {'error': 'Password must contain at least one special character.'})
       
        hashed_password = make_password(password)
        
        user = CustomUser.objects.get(email=email)
        user.password = hashed_password
        user.save()
        return redirect('login')
    else:
        return render(request, 'create_password_.html', {'count': count})
@login_required(login_url='home')
def donated_pets(request):
    user_id = request.user.id
    count = Donor_message.objects.filter(user_id=user_id,visited=False).count()
    if request.user.is_authenticated:
        donated_pets = Pet.objects.filter(donor=request.user)
        return render(request, 'donated_pets.html', {'donated_pets': donated_pets,'count':count})
    else:
        return redirect('login')
@login_required(login_url='home')
def edit_donated_pet(request, pet_id):
    user_id = request.user.id
    count = Donor_message.objects.filter(user_id=user_id,visited=False).count()
    
    pet = get_object_or_404(Pet, id=pet_id)
    
    
    if request.method == 'POST':
        pet_name = request.POST.get('pet_name')
        pet_breed = request.POST.get('pet_breed')
        pet_age = request.POST.get('pet_age')
        pet_category_id = request.POST.get('pet_category')
        pet_image = request.FILES.get('pet_image')
        
        
        pet.pet_name = pet_name
        pet.pet_breed = pet_breed
        pet.pet_age = pet_age
        if pet_image:
            pet.pet_image = pet_image
        pet.cat = Category.objects.get(id=pet_category_id)
        
        
        pet.save()
        messages.success(request, 'Pet details updated successfully!')
        return redirect('donated_pets')
    categories = Category.objects.all()
    return render(request, 'edit_donated_pets.html', {'pet': pet, 'categories': categories,'count':count})
@login_required(login_url='home')
def delete_donated_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    
    pet.delete()
    
    messages.success(request, 'Pet deleted successfully!')
    
    return redirect('donated_pets')   
def donor_notification(request):
    user_id = request.user.id
    count = Donor_message.objects.filter(user_id=user_id,visited=False).count()
    user_id = request.user.id
    
    
    cart_items = Cart.objects.filter(donor_id=user_id)
    
    
    for item in cart_items:
        item.visited = True
        item.save()
   
    return render(request, 'notifications.html', {'cart_items': cart_items,'count':count})
def donor_notifi(request):
    user_id = request.user.id
    count = Donor_message.objects.filter(user_id=user_id,visited=False).count()
    return render(request,'donor_notifi.html',{'count':count})

    












