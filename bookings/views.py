from django.shortcuts import render, redirect
from .forms import AppointmentForm
from .models import Appointment, Service


def home(request):
    return render(request, "bookings/home.html")


def book_appointment(request):
    service_name = request.GET.get("service")

    if request.method == "POST":
        form = AppointmentForm(request.POST)

        if form.is_valid():
            appointment = form.save()

            request.session["appointment_id"] = appointment.id
            return redirect("booking_success")
    else:
        if service_name:
            try:
                service = Service.objects.get(
                    name=service_name,
                    is_active=True
                )
                form = AppointmentForm(initial={"service": service})
            except Service.DoesNotExist:
                form = AppointmentForm()
        else:
            form = AppointmentForm()

    return render(
        request,
        "bookings/book_appointment.html",
        {"form": form}
    )

def booking_success(request):
    appointment_id = request.session.get("appointment_id")

    if not appointment_id:
        return redirect("book_appointment")
    
    appointment = Appointment.objects.get(id=appointment_id)
    return render(request, "bookings/booking_success.html", {"appointment": appointment})

def about(request):
    return render(request, "bookings/about.html")

def contact(request):
    return render(request, "bookings/contact.html")