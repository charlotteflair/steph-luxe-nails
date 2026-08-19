from django import forms
from .models import Appointment


class AppointmentForm(forms.ModelForm):
    SERVICE_PRICES = {
    "Basic Manicure": "₦5,000",
    "Gel Manicure": "₦6,000",
    "Builder Gel (BIAB)": "₦7,500",
    "Basic Pedicure": "₦5,000",
    "Callus Treatment": "₦10,000",
    "Acrylic Nails": "₦12,000 - ₦18,000",
    "Gel Nails": "₦8,000 - ₦12,000",
    "Square Nails": "₦7,000",
    "Oval Nails": "₦9,000",
    "Coffin Nails": "₦10,000",
    "Nail Arts": "₦5,000",
}
    class Meta:
        model = Appointment
        fields = [
            "customer_name",
            "customer_email",
            "customer_phone",
            "service",
            "nail_technician",
            "appointment_date",
            "start_time",
            "end_time",
            "notes",
        ]

        widgets = {
            "appointment_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "start_time": forms.TimeInput(
                attrs={"type": "time"}
            ),
            "end_time": forms.TimeInput(
                attrs={"type": "time"}
            ),
            "notes": forms.Textarea(
                attrs={"rows": 4}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        field = self.fields.get("service")
        if field is not None and hasattr(field, "queryset"):
            def label_from_instance(obj):
                price = self.SERVICE_PRICES.get(getattr(obj, "name", ""), "")
                return f"{obj.name} — {price}" if price else obj.name

            field.label_from_instance = label_from_instance

    def clean(self):
        cleaned_data = super().clean()

        technician = cleaned_data.get("nail_technician")
        appointment_date = cleaned_data.get("appointment_date")
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if technician and appointment_date and start_time and end_time:

            if end_time <= start_time:
                raise forms.ValidationError(
                    "End time must be later than start time."
                )

            overlapping_appointments = Appointment.objects.filter(
                nail_technician=technician,
                appointment_date=appointment_date,
                start_time__lt=end_time,
                end_time__gt=start_time,
            ).exclude(status="cancelled")

            if self.instance.pk:
                overlapping_appointments = overlapping_appointments.exclude(
                    pk=self.instance.pk
                )

            if overlapping_appointments.exists():
                raise forms.ValidationError(
                    "Sorry, this nail technician is already booked "
                    "for this time. Please choose another time."
                )

        return cleaned_data