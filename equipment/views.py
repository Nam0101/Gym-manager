# Create your views here.
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.signals import post_save
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from equipment.forms import SearchForm, EquipmentForm
from equipment.models import Equipment
from members.models import Manager
from notifications.config import my_handler

# views.py
from .forms import EquipmentForm
from .models import STATUS_CHOICES


def model_save(model):
    post_save.disconnect(my_handler, sender=Equipment)
    model.save()
    post_save.connect(my_handler, sender=Equipment)


def view_equipment(request):
    search_form = SearchForm()
    current_user = request.user
    if current_user.is_superuser:
        view_all = Equipment.objects.all().order_by('-id')
    else:
        current_manager = Manager.objects.get(user=current_user)
        current_room = current_manager.room
        view_all = Equipment.objects.filter(room=current_room).order_by('-id')
    paginator = Paginator(view_all, 10)
    try:
        page = request.GET.get('page', 1)
        view_all = paginator.page(page)
    except PageNotAnInteger:
        view_all = paginator.page(1)
    except EmptyPage:
        view_all = paginator.page(paginator.num_pages)
    context = {'result': view_all, 'search_form': search_form}
    return render(request, "view_equipment.html", context)


def add_equipment(request):
    current_user = request.user
    if request.method == 'POST':
        form = EquipmentForm(request.POST, user=current_user)
        if form.is_valid():
            equipment_code = form.cleaned_data.get('equipment_code')
            if Equipment.objects.filter(equipment_code=equipment_code).exists():
                messages.error(request, f"An equipment with code {equipment_code} already exists.")
            else:
                form.save()
                return redirect('view_equipment')
    else:
        form = EquipmentForm(user=current_user)
    context = {'form': form, 'STATUS_CHOICES': STATUS_CHOICES}
    return render(request, "add_equipment.html", context)


def search_equipment(request):
    form = SearchForm(request.POST or None)
    if form.is_valid():
        search_query = form.cleaned_data.get('search')
        results = Equipment.objects.filter(equipment_name__icontains=search_query)
        context = {'form': form, 'results': results}
        return render(request, 'search_results.html', context)
    else:
        context = {'form': form}
        return render(request, 'search_form.html', context)


def update_equipment(request, equipment_id):
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    current_user = request.user
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment, user=current_user)
        if form.is_valid():
            form.save()
            return redirect('view_equipment')
    else:
        form = EquipmentForm(instance=equipment, user=current_user)
    context = {'form': form}
    return render(request, 'update_equipment.html', context)
