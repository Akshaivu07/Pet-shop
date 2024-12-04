from django.urls import path
from .import views

urlpatterns = [
    
    path('adoptor_reg',views.adoptor_reg,name='adoptor_reg'),
    path('a_reg_db',views.a_reg_db,name='a_reg_db'),
    path('generate_otp_a',views.generate_otp_a,name='generate_otp_a'),
    
    path('adoptor_home',views.adoptor_home,name='adoptor_home'),
    path('view_approved',views.view_approved,name='view_approved'),
    path('pet_details<int:pet_id>',views.pet_details,name='pet_details'),
    path('adopt_details<int:pet_id>',views.adopt_details,name='adopt_details'),
    path('u_password',views.u_password,name='u_password'),
    path('set_password',views.set_password,name='set_password'),
    path('confirm_adopt<int:pet_id>',views.confirm_adopt,name='confirm_adopt'),
    
    
    path('user_notification',views.user_notification,name='user_notification'),
    path('admin_notification',views.admin_notification,name='admin_notification'),
    path('adoptor_details/<int:adoptor_id>/', views.adoptor_details, name='adoptor_details'),
    path('user_profile_view',views.user_profile_view,name='user_profile_view'),
    path('user_pro_edit/<int:pk>',views.user_pro_edit,name='user_pro_edit'),
    path('user_profile_edit/<int:pk>',views.user_profile_edit,name='user_profile_edit'),
    path('view_adopted_pets',views.view_adopted_pets,name='view_adopted_pets'),
    path('donor_notifi',views.donor_notifi,name='donor_notifi'),



    

]