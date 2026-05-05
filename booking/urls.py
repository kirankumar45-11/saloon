from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Expert Auth
    path('expert/register/', views.expert_register, name='expert_register'),
    path('expert/login/', views.expert_login, name='expert_login'),

    # Customer Auth
    path('register/', views.customer_register, name='customer_register'),
    path('login/', views.customer_login, name='customer_login'),
    path('logout/', views.logout_view, name='logout'),

    # Customer pages
    path('book/', views.book_appointment, name='book'),
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('profile/', views.customer_profile_view, name='customer_profile'),

    # Expert pages
    path('expert/dashboard/', views.expert_dashboard, name='expert_dashboard'),
    path('expert/appointment/<int:pk>/<str:action>/', views.appointment_action, name='appointment_action'),
    path('experts/', views.expert_list, name='expert_list'),
    path('expert/profile/', views.expert_profile_view, name='expert_profile'),

    # Payment & Invoice
    path('payment/<int:appointment_id>/', views.payment_page, name='payment'),
    path('invoice/<int:payment_id>/', views.invoice, name='invoice'),

    # APIs
    path('api/services/<int:category_id>/', views.get_services, name='get_services'),
    path('api/availability/<int:expert_id>/', views.get_expert_availability, name='get_expert_availability'),
    path('api/availability/all/', views.get_salon_availability, name='get_salon_availability'),
]
