import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salon_project.settings')
django.setup()

from django.contrib.auth.models import User
from booking.models import Expert, CustomerProfile, ServiceCategory, Service


def seed():
    print("-- Seeding database --")

    # Superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("[OK] Superuser: admin / admin123")

    # -- Experts --
    experts_data = [
        {'username': 'elena', 'first': 'Elena', 'last': 'Rossi', 'email': 'elena@salon.com',
         'exp': 10, 'spec': 'Hair Coloring, Balayage',
         'bio': 'Expert colorist with 10 years of experience in balayage and highlights.',
         'image': 'expert_elena.png'},
        {'username': 'marcus', 'first': 'Marcus', 'last': 'Johnson', 'email': 'marcus@salon.com',
         'exp': 8, 'spec': 'Barbering, Men\'s Grooming',
         'bio': 'Master barber specializing in fades, beard trims, and classic cuts.',
         'image': 'expert_marcus.png'},
        {'username': 'sophia', 'first': 'Sophia', 'last': 'Lee', 'email': 'sophia@salon.com',
         'exp': 5, 'spec': 'Spa, Facials, Massage',
         'bio': 'Certified massage therapist and facial specialist.',
         'image': 'expert_sophia.png'},
    ]
    for ed in experts_data:
        if not User.objects.filter(username=ed['username']).exists():
            user = User.objects.create_user(
                username=ed['username'], email=ed['email'], password='expert123',
                first_name=ed['first'], last_name=ed['last']
            )
            Expert.objects.create(
                user=user, experience_years=ed['exp'],
                specialization=ed['spec'], bio=ed['bio'],
                static_image=ed['image']
            )
            print(f"[OK] Expert: {ed['username']} / expert123")
        else:
            # Update existing expert with image
            try:
                expert = User.objects.get(username=ed['username']).expert_profile
                expert.static_image = ed['image']
                expert.save()
                print(f"[OK] Updated image for: {ed['username']}")
            except Exception:
                pass

    # -- Categories & Services --
    hair, _ = ServiceCategory.objects.get_or_create(
        name='Hair Care',
        defaults={'description': 'Cuts, styling, and coloring.', 'icon': 'fa-scissors', 'image': 'service_haircare.png'}
    )
    if not hair.image:
        hair.image = 'service_haircare.png'
        hair.save()

    spa, _ = ServiceCategory.objects.get_or_create(
        name='Spa & Relax',
        defaults={'description': 'Massages, facials, and treatments.', 'icon': 'fa-spa', 'image': 'service_spa.png'}
    )
    if not spa.image:
        spa.image = 'service_spa.png'
        spa.save()

    beauty, _ = ServiceCategory.objects.get_or_create(
        name='Beauty',
        defaults={'description': 'Makeup, nails, and skincare.', 'icon': 'fa-wand-magic-sparkles', 'image': 'service_beauty.png'}
    )
    if not beauty.image:
        beauty.image = 'service_beauty.png'
        beauty.save()

    services = [
        (hair, "Men's Haircut", 'Classic or modern men\'s haircut.', 30, 30),
        (hair, "Women's Haircut", 'Includes wash, cut, and blow-dry.', 60, 60),
        (hair, 'Balayage Coloring', 'Full balayage color treatment.', 150, 120),
        (hair, 'Hair Straightening', 'Keratin smoothing treatment.', 120, 90),
        (spa, 'Deep Tissue Massage', '60-minute deep tissue massage.', 80, 60),
        (spa, 'Hydrating Facial', 'Skin-refreshing facial treatment.', 50, 45),
        (spa, 'Hot Stone Massage', 'Relaxing hot stone therapy.', 100, 75),
        (beauty, 'Bridal Makeup', 'Complete bridal makeup session.', 200, 120),
        (beauty, 'Manicure & Pedicure', 'Full nail care package.', 45, 60),
    ]
    for cat, name, desc, price, dur in services:
        Service.objects.get_or_create(
            category=cat, name=name,
            defaults={'description': desc, 'price': price, 'duration_minutes': dur}
        )

    print("[OK] Categories & services seeded")
    print("-- Done! --")


if __name__ == '__main__':
    seed()
