from django.urls import path
from .views import *

app_name = 'inventory'

urlpatterns = [
    path("", MainInventory, name="home"),
    path("device-and-serials/", DeviceAndSerials, name="DeviceAndSerials"),
    # path("overdue/", send_overdue_reservation_emails, name="overdue"),
    path("student-dashboard/", student_dashboard, name="student_dashboard"),
    path("type/<int:type_id>", equipment_in_type, name="equipment_in_type"),
    path('reservation/<str:equipment_type>/<int:equipment_id>/', reservation_view, name='reservation_view'),
    path('delete-reservation/<int:reservation_id>', delete_reservation_view, name='delete_reservation_view'),
    path("equipment-type/<int:type_id>", equipment_in_type, name="equipment_in_type"),
    path("device-type/<int:type_id>", device_in_type, name="device_in_type"),
    path('search/', search_view, name='search_view'),
    path('search-device/', device_search_view, name='device_search_view'),
]
