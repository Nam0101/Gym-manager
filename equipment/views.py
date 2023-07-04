# Create your views here.
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.signals import post_save
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from equipment.forms import SearchForm, EquipmentForm
from equipment.models import Equipment
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
    view_all = Equipment.objects.all()
    paginator = Paginator(view_all, 100)
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
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            equipment_code = form.cleaned_data.get('equipment_code')
            if Equipment.objects.filter(equipment_code=equipment_code).exists():
                messages.error(request, f"An equipment with code {equipment_code} already exists.")
            else:
                form.save()
                return redirect('view_equipment')
    else:
        form = EquipmentForm()
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
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            return redirect('view_equipment')
    else:
        form = EquipmentForm(instance=equipment)
    context = {'form': form}
    return render(request, 'update_equipment.html', context)
