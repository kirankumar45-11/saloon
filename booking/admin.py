from django.contrib import admin
from .models import Expert, CustomerProfile, ServiceCategory, Service, Appointment, Payment, Bill


@admin.register(Expert)
class ExpertAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'experience_years', 'is_available')
    list_filter = ('is_available', 'specialization')


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'duration_minutes')
    list_filter = ('category',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'expert', 'service', 'date', 'time', 'status')
    list_filter = ('status', 'date', 'expert')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'total_amount', 'paid_amount', 'payment_type', 'status')
    list_filter = ('status', 'payment_type')


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('bill_number', 'payment', 'created_at')
