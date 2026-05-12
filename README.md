📱 Salon Booking Management System

A full-stack Salon Booking Web Application built using Django (Python) for backend and HTML, CSS, JavaScript for frontend.
This system allows customers to book salon services online and enables salon experts to manage appointment requests efficiently.

🚀 Overview

This project digitizes the traditional salon booking process by providing:

Online appointment scheduling
Expert (Stylist) registration and dashboard
Booking request management
Payment simulation
Invoice (Bill) generation

The application improves efficiency, reduces manual work, and enhances user experience through a simple and responsive interface.

✨ Features
👤 Authentication
User login system using Django authentication
Expert registration with experience and specialization
📅 Booking System
Select service, date, and time
Store booking details in database
Prevent invalid inputs and scheduling conflicts
📋 Expert Dashboard
View booking requests
Accept or reject requests
Manage appointment status
💳 Payment Module
Simulated payment process
Updates payment status
🧾 Invoice Generation
Generates bill after payment
Displays service and payment details
Print invoice option
🏗️ Tech Stack
Layer	Technology
Backend	Django (Python)
Frontend	HTML, CSS, JavaScript
Database	SQLite
Tools	VS Code, Git, GitHub
📂 Project Structure
salon_project/
│
├── salon/
│   ├── models.py        # Database models
│   ├── views.py         # Application logic
│   ├── urls.py          # URL routing
│   ├── forms.py         # Forms
│
├── templates/
│   ├── register_expert.html
│   ├── login.html
│   ├── booking.html
│   ├── expert_dashboard.html
│   ├── payment.html
│   ├── invoice.html
│
├── static/              # CSS, JS files
├── manage.py
⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/kirankumar45-11/saloon.git
cd saloon
2️⃣ Create Virtual Environment
python -m venv env
Activate Environment
Windows
env\Scripts\activate
Mac/Linux
source env/bin/activate
3️⃣ Install Dependencies
pip install django
4️⃣ Apply Migrations
python manage.py makemigrations
python manage.py migrate
5️⃣ Run the Server
python manage.py runserver

Open in browser:

👉 http://127.0.0.1:8000/

📊 Modules
Expert Module – Registration & login
Customer Module – Booking services
Booking Module – Appointment management
Payment Module – Payment handling
Billing Module – Invoice generation
📄 Project Report

A complete detailed Project Report is also uploaded in this GitHub repository.

The report includes:

Abstract
Introduction
Objectives
Problem Statement
System Analysis & Design
Module Description
Database Design
Implementation
Testing
Advantages & Limitations
Future Enhancements
Conclusion

You can refer to the uploaded report document for detailed project explanation and documentation.

📌 Future Enhancements
🔐 OTP-based login
💳 Real payment gateway integration (Razorpay/Stripe)
📩 Email/SMS notifications
⭐ Ratings & reviews system
📱 Mobile application version
🤖 AI-based stylist recommendation
👨‍💻 Team Details
Team Number

Team 07

Team Members
R Kiran Kumar
Shivakumar B V
Vijayasree K
Tejeshwar M
Neha Savakar
Syed Sajith Ahamed S
Rakshitha
Ayesha
🙌 Author

R Kiran Kumar
CSE Student

GitHub:
https://github.com/kirankumar45-11

Project Repository:
https://github.com/kirankumar45-11/saloon
