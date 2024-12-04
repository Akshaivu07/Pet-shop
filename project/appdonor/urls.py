from django.urls import path
from .import views

urlpatterns = [
    
    path('donor_reg',views.donor_reg, name='donor_reg'),
    path('d_reg_db',views.d_reg_db,name='d_reg_db'),
    path('generate_otp',views.generate_otp,name='generate_otp'),
   
    path('donor_home',views.donor_home,name='donor_home'),
    
    path('donor_form',views.donor_form,name='donor_form'),
    path('pet_db',views.pet_db,name='pet_db'),
    path('edit_donor_profile/<int:pk>/', views.edit_donor_profile, name='edit_donor_profile'),

    path('d_password',views.d_password,name='d_password'),
    path('set_password_d',views.set_password_d,name='set_password_d'),
    path('show_donation_messages',views.show_donation_messages,name='show_donation_messages'),
    path('donated_pets',views.donated_pets,name='donated_pets'),
    path('delete_donated_pet/<int:pet_id>',views.delete_donated_pet,name='delete_donated_pet'),
    path('edit_donated_pet/<int:pet_id>',views.edit_donated_pet,name='edit_donated_pet'),
    path('view_donor_profile',views.view_donor_profile,name='view_donor_profile'),
    path('edit_donor_pro/<int:pk>',views.edit_donor_pro,name='edit_donor_pro'),
    path('donor_notification',views.donor_notification,name='donor_notification'),
    path('donor_notifi',views.donor_notifi,name='donor_notifi'),
    
    

    

]