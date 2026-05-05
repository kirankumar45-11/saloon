from django.db import models
from django.contrib.auth.models import User


class Expert(models.Model):
    """Salon Expert / Stylist model with its own auth linked to User."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='expert_profile')
    phone = models.CharField(max_length=20, blank=True)
    experience_years = models.IntegerField(default=0)
    specialization = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='experts/', blank=True, null=True)
    static_image = models.CharField(max_length=100, blank=True, help_text='Filename in static/images/')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class CustomerProfile(models.Model):
    """Customer profile linked to User."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class ServiceCategory(models.Model):
    """Top-level service category (e.g. Hair Care, Spa)."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text='Font Awesome icon class')
    image = models.CharField(max_length=100, blank=True, help_text='Filename in static/images/')

    class Meta:
        verbose_name_plural = 'Service Categories'

    def __str__(self):
        return self.name


class Service(models.Model):
    """Specific service offered (e.g. Men's Haircut)."""
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_minutes = models.IntegerField(default=30)

    def __str__(self):
        return f"{self.name} (${self.price})"


class Appointment(models.Model):
    """Booking between a customer and an expert."""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_appointments')
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE, related_name='expert_appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.customer.username} → {self.expert} on {self.date} at {self.time}"


class Payment(models.Model):
    """Payment record for an appointment."""
    TYPE_CHOICES = [
        ('FULL', 'Full Payment'),
        ('ADVANCE', 'Advance Payment'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='payment')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='FULL')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    method = models.CharField(max_length=50, default='Card')
    transaction_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment #{self.pk} - {self.status}"


class Bill(models.Model):
    """Invoice / Bill generated after payment."""
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='bill')
    bill_number = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bill {self.bill_number}"
