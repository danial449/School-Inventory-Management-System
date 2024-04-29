from django.contrib import admin
from .models import *
from django.core.mail import send_mail
from django.conf import settings
# Register your models here.

class MainEquipmentAdmin(admin.ModelAdmin):
    list_display = ( 'id' , 'name' , 'type' , 'quantity' , 'audit' , 'location' , 'status')

    list_display_links = ('id' , 'name')
    
    list_filter = ('type', 'status')

    search_fields =('name' ,'audit' , 'location')

admin.site.register(MainEquipment , MainEquipmentAdmin)

class EquipmentAdmin(admin.ModelAdmin):
    list_display = ( 'id' , 'name' , 'type' , 'serial_no' , 'CPU' , 'GPU' , 'RAM' , 'availability')

    list_display_links = ('id' , 'name')
    
    list_filter = ('type', 'availability')

    search_fields =('name' , 'serial_no' , 'CPU' , 'GPU' , 'RAM')

admin.site.register(Equipment , EquipmentAdmin)

class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ('id' , 'name', 'display_equipments')

    list_display_links = ('id' , 'name')

    search_fields =('name',)

    def display_equipments(self, obj):
        # Get the equipments related to this type
        equipments = Equipment.objects.filter(type=obj)
        # Return a comma-separated list of service titles
        return ", ".join([equipment.name for equipment in equipments])

    # Set a more descriptive column header
    display_equipments.short_description = 'Equipments in Category'

admin.site.register(EquipmentType , EquipmentTypeAdmin)


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name' , 'last_name', 'username' , 'get_equipment_name' , 'registration_no' , 'return_date',  'status')

    actions = ['send_overdue_reservation_emails']

    list_display_links = ('id' , 'first_name' , 'last_name', 'username')
    
    list_filter = ('status',)

    search_fields =('first_name' , 'last_name', 'username' , 'email' , 'registration_no' , 'return_date')

    def get_equipment_name(self, obj):
        if obj.content_type.model_class() is not None:
            return obj.content_type.get_object_for_this_type(id=obj.object_id).name
        return "N/A"

    get_equipment_name.short_description = 'Equipment'

    def send_overdue_reservation_emails(self, request, queryset):
        overdue_reservations = queryset.filter(return_date__lt=timezone.now(), status='Reserved')
        for reservation in overdue_reservations:
            subject = 'Overdue Reservation Reminder'
            message = f'Your reservation for {reservation.equipment.name} is overdue. Please return it as soon as possible.'
            email_from = settings.DEFAULT_FROM_EMAIL
            recipient_list = [reservation.email]
            send_mail(subject, message, email_from, recipient_list)
        self.message_user(request, "Emails sent successfully for overdue reservations")
    send_overdue_reservation_emails.short_description = "Send Overdue Reservation Emails"
admin.site.register(Reservation, ReservationAdmin)