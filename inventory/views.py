from django.shortcuts import render , redirect , get_object_or_404 , HttpResponse
from .models import *
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from django.db.models import Count
from django.contrib.auth.decorators import login_required
# Create your views here.


def MainInventory(request):
    sort_by = request.GET.get('sort_by', '-id')  # Default sorting by id descending
    equipments = MainEquipment.objects.all().order_by(sort_by)
    types = EquipmentType.objects.annotate(main_equipments_count=Count('main_equipments')).filter(main_equipments_count__gt=0)
    # pagination of services
    paginator = Paginator(equipments , 8)
    page_number = request.GET.get('page')
    equipmentfinal = paginator.get_page(page_number)
    totalpage = equipmentfinal.paginator.num_pages

    context ={
        'main_equipments':equipmentfinal,
        'types':types,
        'current_sorting': sort_by,
        'totalpagelist' : [n+1 for n in range(totalpage)]
    }
    return render(request , "inventory/home.html", context)

def equipment_in_type(request , type_id):
    sort_by = request.GET.get('sort_by', '-id')  # Default sorting by id descending
    types = EquipmentType.objects.annotate(main_equipments_count=Count('main_equipments')).filter(main_equipments_count__gt=0)
    type = EquipmentType.objects.get(id=type_id)
    equipments = type.main_equipments.all().order_by(sort_by)

    context = {
        'main_equipments':equipments,
        'types':types,
        'type' : type,
        'current_sorting': sort_by,
    }
    return render(request , "inventory/equipments_in_type.html" , context)

def DeviceAndSerials(request):
    sort_by = request.GET.get('sort_by', '-id')  # Default sorting by id descending
    equipments = Equipment.objects.all().order_by(sort_by)
    types = EquipmentType.objects.annotate(equipments_count=Count('equipments')).filter(equipments_count__gt=0)
    # pagination of services
    paginator = Paginator(equipments , 10)
    page_number = request.GET.get('page')
    equipmentfinal = paginator.get_page(page_number)
    totalpage = equipmentfinal.paginator.num_pages

    context ={
        'equipments':equipmentfinal,
        'types':types,
        'current_sorting': sort_by,
        'totalpagelist' : [n+1 for n in range(totalpage)]
    }
    return render(request , "inventory/deviceAndserials.html", context)

def device_in_type(request , type_id):
    sort_by = request.GET.get('sort_by', '-id')  # Default sorting by id descending
    types = EquipmentType.objects.annotate(equipments_count=Count('equipments')).filter(equipments_count__gt=0)
    type = EquipmentType.objects.get(id=type_id)
    device_equipments = type.equipments.all().order_by(sort_by)

    context = {
        'types':types,
        'type' : type,
        'current_sorting': sort_by,
        'equipments': device_equipments,
    }
    
    return render(request , "inventory/device_in_type.html" , context)
@login_required
def reservation_view(request, equipment_type, equipment_id):
    if equipment_type == 'Equipment':
        model = Equipment
    elif equipment_type == 'MainEquipment':
        model = MainEquipment

    equipment = get_object_or_404(model, id=equipment_id)

    if request.method == 'POST':
        user = request.user
        status = 'Requested'

        reservation = Reservation(
            equipment_type=equipment_type,
            content_type=ContentType.objects.get_for_model(model),
            object_id=equipment.id,
            equipment=equipment,
            user=user,
            email=user.email,
            registration_no=user.registration_no,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            status=status
        )
        reservation.return_date = timezone.now() + timedelta(days=1)  # Set return date to one day from now  # Set return date
        reservation.save()
        messages.success(request, "Successfully Reserved")

        current_site = get_current_site(request)
        subject = 'New Reservation'
        reservation_link = f'http://{current_site}/admin/inventory/reservation/'
        message = f'\n Name : {user.first_name} {user.last_name} \n Equipment : {equipment} \n click the link to check reservation:{reservation_link}'
        email_from = settings.DEFAULT_FROM_EMAIL
        recipeient_list = ['admin@gmail.com']
        send_mail(subject, message, email_from, recipeient_list)
        return redirect('inventory:student_dashboard')

    return render(request, 'inventory/student_dashboard.html', {'equipment': equipment})
@login_required
def delete_reservation_view(request , reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    reservation.delete()
    messages.success(request, "Reservation successfully cancelled. If you need further assistance, feel free to contact us.")
    return redirect('inventory:student_dashboard')
@login_required
def student_dashboard(request):
    user_reservations = Reservation.objects.filter(user=request.user).order_by('-id')
    has_requested_reservations = user_reservations.filter(status='Requested').exists()
    context = {
        'has_requested_reservations': has_requested_reservations,
        'user_reservations': user_reservations
    }
    return render(request, 'inventory/student_dashboard.html', context)

# def send_overdue_reservation_emails(request):
#     overdue_reservations = Reservation.objects.filter(return_date__lt=timezone.now(), status='Reserved')
#     print(overdue_reservations)
#     for reservation in overdue_reservations:
#         subject = 'Overdue Reservation Reminder'
#         message = f'Your reservation for {reservation.equipment.name} is overdue. Please return it as soon as possible.'
#         email_from = settings.DEFAULT_FROM_EMAIL
#         recipient_list = [reservation.email]
#         send_mail(subject, message, email_from, recipient_list)
#     return HttpResponse("Emails sent successfully for overdue reservations")


from django.db.models import Q

def search_view(request):
    query = request.GET.get('q')

    if query:
        main_equipments = MainEquipment.objects.filter(
            Q(name__icontains=query) |
            Q(location__icontains=query) |
            Q(status__icontains=query)
        )
        context = {
            'main_equipments': main_equipments,
            'query': query,
        }
        return render(request, 'inventory/search_results.html', context)
    else:
        messages.info(request, "Please enter a search query.")
        
    return redirect('inventory:home')


def device_search_view(request):
    query = request.GET.get('q')

    if query:
        equipments = Equipment.objects.filter(
            Q(name__icontains=query) |
            Q(serial_no__icontains=query) |
            Q(CPU__icontains=query) |
            Q(GPU__icontains=query) |
            Q(RAM__icontains=query)
        )
        context = {
            'equipments': equipments,
            'query': query,
        }
        return render(request, 'inventory/device_search_result.html', context)
    else:
        messages.info(request, "Please enter a search query.")
        
    return redirect('inventory:device_search_view')

