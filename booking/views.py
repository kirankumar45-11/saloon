import uuid
from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from .models import (
    Expert, CustomerProfile, ServiceCategory, Service,
    Appointment, Payment, Bill,
)
from .forms import ExpertRegistrationForm, CustomerRegistrationForm, AppointmentForm


# ─────────────────────────────────────────────
#  HOME
# ─────────────────────────────────────────────
def home(request):
    categories = ServiceCategory.objects.all()
    experts = Expert.objects.filter(is_available=True)[:6]
    return render(request, 'home.html', {'categories': categories, 'experts': experts})


# ─────────────────────────────────────────────
#  EXPERT AUTH
# ─────────────────────────────────────────────
def expert_register(request):
    if request.method == 'POST':
        form = ExpertRegistrationForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            user = _create_user(d)
            Expert.objects.create(
                user=user,
                phone=d.get('phone', ''),
                experience_years=d['experience_years'],
                specialization=d['specialization'],
                bio=d.get('bio', ''),
            )
            messages.success(request, 'Expert account created! Please log in.')
            return redirect('expert_login')
    else:
        form = ExpertRegistrationForm()
    return render(request, 'expert_register.html', {'form': form})


def expert_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and hasattr(user, 'expert_profile'):
            login(request, user)
            return redirect('expert_dashboard')
        messages.error(request, 'Invalid credentials or not an expert account.')
    return render(request, 'expert_login.html')


# ─────────────────────────────────────────────
#  CUSTOMER AUTH
# ─────────────────────────────────────────────
def customer_register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            user = _create_user(d)
            CustomerProfile.objects.create(user=user, phone=d.get('phone', ''))
            messages.success(request, 'Account created! Please log in.')
            return redirect('customer_login')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'customer_register.html', {'form': form})


def customer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and hasattr(user, 'customer_profile'):
            login(request, user)
            return redirect('customer_dashboard')
        messages.error(request, 'Invalid credentials or not a customer account.')
    return render(request, 'customer_login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


# ─────────────────────────────────────────────
#  STYLIST / EXPERT LISTING
# ─────────────────────────────────────────────
def expert_list(request):
    experts = Expert.objects.filter(is_available=True)
    return render(request, 'expert_list.html', {'experts': experts})


# ─────────────────────────────────────────────
#  CUSTOMER: BOOKING
# ─────────────────────────────────────────────
@login_required(login_url='customer_login')
def book_appointment(request):
    if not hasattr(request.user, 'customer_profile'):
        messages.error(request, 'Only customers can book appointments.')
        return redirect('home')

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save(commit=False)
            appt.customer = request.user

            # Prevent past dates
            if appt.date < date.today():
                messages.error(request, 'Cannot book a past date.')
            # Prevent double booking
            elif Appointment.objects.filter(
                expert=appt.expert, date=appt.date, time=appt.time,
                status__in=['PENDING', 'ACCEPTED']
            ).exists():
                messages.error(request, 'This expert is already booked at that date & time.')
            else:
                appt.save()
                messages.success(request, 'Appointment request sent! The expert will confirm it.')
                return redirect('customer_dashboard')
    else:
        form = AppointmentForm()

    categories = ServiceCategory.objects.all()
    return render(request, 'book.html', {'form': form, 'categories': categories})


# ─────────────────────────────────────────────
#  CUSTOMER: DASHBOARD
# ─────────────────────────────────────────────
@login_required(login_url='customer_login')
def customer_dashboard(request):
    appointments = Appointment.objects.filter(customer=request.user)
    return render(request, 'customer_dashboard.html', {'appointments': appointments})


# ─────────────────────────────────────────────
#  EXPERT: DASHBOARD  (Accept / Reject)
# ─────────────────────────────────────────────
@login_required(login_url='expert_login')
def expert_dashboard(request):
    if not hasattr(request.user, 'expert_profile'):
        messages.error(request, 'Access denied.')
        return redirect('home')
    expert = request.user.expert_profile
    appointments = Appointment.objects.filter(expert=expert)
    return render(request, 'expert_dashboard.html', {'appointments': appointments, 'expert': expert})


@login_required(login_url='expert_login')
def appointment_action(request, pk, action):
    """Expert accepts or rejects a booking request."""
    appt = get_object_or_404(Appointment, pk=pk)
    if not hasattr(request.user, 'expert_profile') or appt.expert != request.user.expert_profile:
        messages.error(request, 'Access denied.')
        return redirect('home')

    if action == 'accept' and appt.status == 'PENDING':
        appt.status = 'ACCEPTED'
        appt.save()
        messages.success(request, f'Appointment with {appt.customer.username} accepted.')
    elif action == 'reject' and appt.status == 'PENDING':
        appt.status = 'REJECTED'
        appt.save()
        messages.info(request, f'Appointment with {appt.customer.username} rejected.')
    return redirect('expert_dashboard')


# ─────────────────────────────────────────────
#  PAYMENT
# ─────────────────────────────────────────────
@login_required(login_url='customer_login')
def payment_page(request, appointment_id):
    appt = get_object_or_404(Appointment, pk=appointment_id, customer=request.user)

    if appt.status != 'ACCEPTED':
        messages.error(request, 'Payment is only available for accepted appointments.')
        return redirect('customer_dashboard')

    if hasattr(appt, 'payment') and appt.payment.status == 'COMPLETED':
        messages.info(request, 'This appointment is already paid.')
        return redirect('invoice', payment_id=appt.payment.pk)

    if request.method == 'POST':
        payment_type = request.POST.get('payment_type', 'FULL')
        total = appt.service.price
        paid = total if payment_type == 'FULL' else round(total * 50 / 100, 2)
        txn_id = f"TXN-{uuid.uuid4().hex[:10].upper()}"

        payment = Payment.objects.create(
            appointment=appt,
            total_amount=total,
            paid_amount=paid,
            payment_type=payment_type,
            status='COMPLETED',
            method=request.POST.get('method', 'Card'),
            transaction_id=txn_id,
        )
        appt.status = 'COMPLETED'
        appt.save()

        # Auto-generate bill
        bill_number = f"INV-{uuid.uuid4().hex[:8].upper()}"
        Bill.objects.create(payment=payment, bill_number=bill_number)

        messages.success(request, 'Payment successful!')
        return redirect('invoice', payment_id=payment.pk)

    return render(request, 'payment.html', {'appointment': appt})


# ─────────────────────────────────────────────
#  INVOICE / BILL
# ─────────────────────────────────────────────
@login_required(login_url='customer_login')
def invoice(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id, appointment__customer=request.user)
    bill = payment.bill
    return render(request, 'invoice.html', {'payment': payment, 'bill': bill})


# ─────────────────────────────────────────────
#  API ENDPOINTS
# ─────────────────────────────────────────────
def get_services(request, category_id):
    services = Service.objects.filter(category_id=category_id).values(
        'id', 'name', 'price', 'duration_minutes'
    )
    return JsonResponse(list(services), safe=False)


def get_expert_availability(request, expert_id):
    """Return booked slots for a given expert on a specific date."""
    req_date = request.GET.get('date')
    if not req_date:
        return JsonResponse([], safe=False)
    booked = Appointment.objects.filter(
        expert_id=expert_id, date=req_date, status__in=['PENDING', 'ACCEPTED']
    ).values_list('time', flat=True)
    return JsonResponse([t.strftime('%H:%M') for t in booked], safe=False)


# ─────────────────────────────────────────────
#  PROFILES
# ─────────────────────────────────────────────
@login_required(login_url='customer_login')
def customer_profile_view(request):
    if not hasattr(request.user, 'customer_profile'):
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    from .profile_forms import UserForm, CustomerProfileForm
    if request.method == 'POST':
        u_form = UserForm(request.POST, instance=request.user)
        p_form = CustomerProfileForm(request.POST, instance=request.user.customer_profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('customer_profile')
    else:
        u_form = UserForm(instance=request.user)
        p_form = CustomerProfileForm(instance=request.user.customer_profile)
    
    return render(request, 'customer_profile.html', {'u_form': u_form, 'p_form': p_form})


@login_required(login_url='expert_login')
def expert_profile_view(request):
    if not hasattr(request.user, 'expert_profile'):
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    from .profile_forms import UserForm, ExpertProfileForm
    if request.method == 'POST':
        u_form = UserForm(request.POST, instance=request.user)
        p_form = ExpertProfileForm(request.POST, request.FILES, instance=request.user.expert_profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('expert_profile')
    else:
        u_form = UserForm(instance=request.user)
        p_form = ExpertProfileForm(instance=request.user.expert_profile)
    
    return render(request, 'expert_profile.html', {'u_form': u_form, 'p_form': p_form})


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def _create_user(data):
    from django.contrib.auth.models import User
    user = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        first_name=data['first_name'],
        last_name=data['last_name'],
    )
    return user
