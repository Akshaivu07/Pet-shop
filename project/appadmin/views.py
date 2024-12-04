from django.shortcuts import render,redirect,get_object_or_404
from appadmin.models import CustomUser,Category,Message,Admin_message,Donation_message
from django.contrib import  messages
from appdonor.models import Pet
from django.contrib.auth import authenticate, login as auth_login
from .models import Message
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from appuser.models import Cart

# Create your views here.
def home(request):
    
    return render(request, 'home.html')


def login(request):
    return render(request,'login.html')




def admin_home(request):
    # Retrieve the count of unvisited donation messages
    messages_count = Donation_message.objects.filter(visited=False).count()
    
    # Pass the count to the template context
    return render(request, 'admin_home.html', {'total_count': messages_count})



def login(request):
    return render(request, 'login.html')



def login1(request):
    if request.method == 'POST':
        username = request.POST.get('lusername')
        password = request.POST.get('lpassword')

        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.user_type == '1':
                return redirect('admin_home')
            elif user.user_type == '2':
                return redirect('donor_home')
            else:
                return redirect('adoptor_home')
        else:
            messages.info(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'home.html')
@login_required(login_url='home')   
def pet_category(request):
    messages_count = Donation_message.objects.filter(visited=False).count()
    return render(request,'pet_category.html',{'count':messages_count})
@login_required(login_url='home')
def add_category(request):
    if request.method == 'POST':
        category = request.POST.get('pet_category')
        
        # Check if the category already exists
        if Category.objects.filter(Category_name=category).exists():
            messages.error(request, f'The category "{category}" already exists.')
        else:
            # If the category doesn't exist, save it
            cat = Category(Category_name=category)
            cat.save()
            messages.success(request, f'Category "{category}" added successfully.')
        
        return redirect('pet_category')
@login_required(login_url='home')
def pet_view(request):
    messages_count = Donation_message.objects.filter(visited=False).count()
    pet=Pet.objects.all()
    return render(request,'donor_view.html',{'pet':pet,'count':messages_count})
@login_required(login_url='home')
def delete(request,pk):
    pet=Pet.objects.get(id=pk)
    pet.delete()
    return redirect('pet_view')
@login_required(login_url='home')   
def approve_pet(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    pet.approved = True
    pet.disapproved = False
    pet.save()
    return redirect('pet_view')

def disapprove_pet(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    pet.approved = False
    pet.disapproved = True
    pet.save()
    return redirect('pet_view')



@login_required(login_url='home')
def is_admin(user):
    return user.is_superuser
def view_users_and_donors(request):
    messages_count = Donation_message.objects.filter(visited=False).count()
    
    users = CustomUser.objects.filter(user_type='3')
    donors = CustomUser.objects.filter(user_type='2')
    
    # Handle user/donor removal if requested
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        try:
            user_to_remove = CustomUser.objects.get(id=user_id)
            user_to_remove.delete()
            messages.success(request, 'User/Donor removed successfully.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'User/Donor not found.')
        return redirect('view_users_and_donors')
    
    # Render the HTML page with the list of users and donors
    return render(request, 'users_details.html', {
        'users': users,
        'donors': donors,
        'count':messages_count
    })

def adoptor_pet_details(request, user_id):
    messages_count = Donation_message.objects.filter(visited=False).count()
    
    user = CustomUser.objects.get(pk=user_id)
    
    adopted_pets = Cart.objects.filter(user=user)  # Assuming you have a 'AdoptedPet' model
    
        
    
    return render(request, 'adoptor_pet_details.html',{'user': user,'adopted_pets': adopted_pets,'count':messages_count})
def donor_pet_details(request, donor_id):
    messages_count = Donation_message.objects.filter(visited=False).count()
    donor = CustomUser.objects.get(pk=donor_id)
    donated_pets = Pet.objects.filter(donor=donor)
    context = {
        'donor': donor,
        'donated_pets': donated_pets,
        'count':messages_count,
    }
    return render(request, 'donor_pet_details.html', context )



@login_required(login_url='home')
def added_category(request):
    messages_count = Donation_message.objects.filter(visited=False).count()
    categories = Category.objects.all()
    return render(request,'added_category.html',{'categories':categories,'count':messages_count})
@login_required(login_url='home')
def edit_category1(request,pk):
    messages_count = Donation_message.objects.filter(visited=False).count()
    category=Category.objects.get(id=pk)
    return render(request,'edit_category.html',{'category':category,'count':messages_count})
@login_required(login_url='home')
def edit_category(request, pk):
    donation_messages_count = Donation_message.objects.filter(visited=False).count()
    category = get_object_or_404(Category, id=pk)
    if request.method == 'POST':
        new_name = request.POST.get('name')
        if new_name and category.Category_name != new_name:
            category.Category_name = new_name
            category.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('added_category')

    
    return render(request, 'edit_category.html', {'category': category,'count':donation_messages_count})
@login_required(login_url='home')
def category_delete(request, pk):
    category = get_object_or_404(Category, id=pk)
    category.delete()
    messages.success(request, 'Category deleted successfully.')
    return redirect('added_category')
@login_required(login_url='home')
def admin_noti(request):
    carts_with_unvisited = Cart.objects.filter(visited2=False)
    pets_with_unvisited = Pet.objects.filter(visited=False)
    
    count_carts = carts_with_unvisited.count()  
    count_pets = pets_with_unvisited.count()
    total_count = count_carts + count_pets
    
    return render(request, 'admin_noti_panel.html', {'count': count_carts, 'count2': count_pets, 'total_count': total_count})
@login_required(login_url='home')
def change_admin_password(request):
    messages_count = Donation_message.objects.filter(visited=False).count()
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('home')

    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if request.user.check_password(current_password):
            
            if new_password == confirm_password:
                request.user.username = new_username
                request.user.set_password(new_password)
                request.user.save()

                
                update_session_auth_hash(request, request.user)

                messages.success(request, 'Username and password have been changed successfully.')
                return redirect('change_admin_password')
            else:
                messages.error(request, 'New password and confirm password do not match.')
        else:
            messages.error(request, 'Current password is incorrect.')

    # Render the change admin credentials form
    return render(request, 'admin_profile_update.html', {'count': messages_count})

from django.db.models import Count

def admin_donor_noti(request):
    # Retrieve all donation messages from the database
    donation_messages = Donation_message.objects.filter(visited=False)
    
    # Calculate the count of donation messages
    donation_messages_count = Donation_message.objects.filter(visited=False).count()
    
    # Update the 'visited' column for each message to True
    
    for message in donation_messages:
        message.visited = True
        message.save()
    
    # Pass the donation messages and count to the template context
    return render(request, 'admin_donor_noti.html', {'notifications': donation_messages, 'count': donation_messages_count})       
