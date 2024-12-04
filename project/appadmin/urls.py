from django.urls import path
from .import views

urlpatterns = [
    
    path('',views.home,name='home'),
    path('admin_home',views.admin_home,name='admin_home'),
    path('login',views.login,name='login'),
    path('login1',views.login1,name='login1'),
    path('pet_category',views.pet_category,name='pet_category'),
    path('add_category',views.add_category,name='add_category'),
    path('pet_view',views.pet_view,name='pet_view'),
    path('approve_pet/<int:pet_id>/', views.approve_pet, name='approve_pet'),
    path('disapprove_pet/<int:pet_id>/', views.disapprove_pet, name='disapprove_pet'),
    path('is_admin',views.is_admin,name='is_admin'),
    path('view_users_and_donors',views.view_users_and_donors,name='view_users_and_donors'),
    path('delete<int:pk>',views.delete,name='delete'),
    path('added_category',views.added_category,name='added_category'),
    path('edit_category1/<int:pk>',views.edit_category1,name='edit_category1'),
    path('edit_category/<int:pk>',views.edit_category,name='edit_category'),
    path('category_delete/<int:pk>',views.category_delete,name='category_delete'),
    path('admin_noti',views.admin_noti,name='admin_noti'),
    path('change_admin_password',views.change_admin_password,name='change_admin_password'),
    path('adoptor-pet-details/<int:user_id>/', views.adoptor_pet_details, name='adoptor_pet_details'),
    path('donor-pet-details/<int:donor_id>/', views.donor_pet_details, name='donor_pet_details'),
    path('admin_donor_noti',views.admin_donor_noti,name='admin_donor_noti'),
    
]
    
    
    

    


