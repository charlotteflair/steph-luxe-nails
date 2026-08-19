from django.contrib import admin
from .models import Service, Appointment, NailTechnician


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "duration", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "customer_name",
        "service",
        "nail_technician",
        "appointment_date",
        "start_time",
        "end_time",
        "status",
    )

    list_filter = (
        "status",
        "appointment_date",
        "nail_technician",
        "service",
    )

    search_fields = (
        "customer_name",
        "customer_email",
        "customer_phone",
    )

    list_editable = ("status",)

    ordering = (
        "appointment_date",
        "start_time",
    )
    list_filter = ("status", "appointment_date")
    search_fields = (
        "customer_name",
        "customer_email",
        "customer_phone",
    )


@admin.register(NailTechnician)
class NailTechnicianAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "phone", "email")
