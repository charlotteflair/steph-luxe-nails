from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("book/", views.book_appointment, name="book_appointment"),
    path("booking-success/", views.booking_success, name="booking_success"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]