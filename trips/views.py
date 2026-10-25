
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import TripForm
from .models import City, PackingItem, Trip


def register(request):
    if request.user.is_authenticated:
        return redirect("trip_list")

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Аккаунт успешно создан.")
            return redirect("trip_list")
    else:
        form = UserCreationForm()

    return render(
        request,
        "registration/register.html",
        {"form": form},
    )


@login_required
def trip_list(request):
    trips = Trip.objects.filter(
        owner=request.user
    ).select_related("country", "city")

    return render(
        request,
        "trips/trip_list.html",
        {"trips": trips},
    )


@login_required
def trip_detail(request, pk):
    trip = get_object_or_404(
        Trip,
        pk=pk,
        owner=request.user,
    )

    packing_items = trip.packing_items.all()
    total_items = packing_items.count()
    packed_items = packing_items.filter(is_packed=True).count()

    return render(
        request,
        "trips/trip_detail.html",
        {
            "trip": trip,
            "packing_items": packing_items,
            "total_items": total_items,
            "packed_items": packed_items,
        },
    )


@login_required
def trip_create(request):
    if request.method == "POST":
        form = TripForm(request.POST)

        if form.is_valid():
            trip = form.save(commit=False)
            trip.owner = request.user
            trip.save()

            messages.success(request, "Поездка успешно создана.")
            return redirect("trip_detail", pk=trip.pk)
    else:
        form = TripForm()

    return render(
        request,
        "trips/trip_form.html",
        {
            "form": form,
            "page_title": "Добавление поездки",
            "button_text": "Создать поездку",
        },
    )


@login_required
def trip_update(request, pk):
    trip = get_object_or_404(
        Trip,
        pk=pk,
        owner=request.user,
    )

    if request.method == "POST":
        form = TripForm(request.POST, instance=trip)

        if form.is_valid():
            form.save()
            messages.success(request, "Поездка успешно изменена.")
            return redirect("trip_detail", pk=trip.pk)
    else:
        form = TripForm(instance=trip)

    return render(
        request,
        "trips/trip_form.html",
        {
            "form": form,
            "trip": trip,
            "page_title": "Редактирование поездки",
            "button_text": "Сохранить изменения",
        },
    )


@login_required
def trip_delete(request, pk):
    trip = get_object_or_404(
        Trip,
        pk=pk,
        owner=request.user,
    )

    if request.method == "POST":
        trip.delete()
        messages.success(request, "Поездка удалена.")
        return redirect("trip_list")

    return render(
        request,
        "trips/trip_confirm_delete.html",
        {"trip": trip},
    )


@login_required
def cities_by_country(request):
    country_id = request.GET.get("country_id")

    if not country_id:
        return JsonResponse({"cities": []})

    cities = City.objects.filter(
        country_id=country_id
    ).values("id", "name")

    return JsonResponse({"cities": list(cities)})


@login_required
def packing_item_add(request, pk):
    trip = get_object_or_404(
        Trip,
        pk=pk,
        owner=request.user,
    )

    if request.method != "POST":
        return redirect("trip_detail", pk=trip.pk)

    name = request.POST.get("name", "").strip()

    if not name:
        return redirect("trip_detail", pk=trip.pk)

    item = PackingItem.objects.create(
        trip=trip,
        name=name,
    )

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        packing_items = trip.packing_items.all()

        return JsonResponse({
            "success": True,
            "item": {
                "id": item.pk,
                "name": item.name,
                "toggle_url": f"/packing/{item.pk}/toggle/",
                "delete_url": f"/packing/{item.pk}/delete/",
            },
            "packed_items": packing_items.filter(is_packed=True).count(),
            "total_items": packing_items.count(),
        })

    return redirect("trip_detail", pk=trip.pk)


@login_required
@require_POST
def packing_item_toggle(request, pk):
    item = get_object_or_404(
        PackingItem,
        pk=pk,
        trip__owner=request.user,
    )

    item.is_packed = not item.is_packed
    item.save(update_fields=["is_packed"])

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        trip = item.trip
        packing_items = trip.packing_items.all()

        return JsonResponse({
            "success": True,
            "is_packed": item.is_packed,
            "packed_items": packing_items.filter(is_packed=True).count(),
            "total_items": packing_items.count(),
        })

    return redirect("trip_detail", pk=item.trip.pk)


@login_required
def packing_item_delete(request, pk):
    item = get_object_or_404(
        PackingItem,
        pk=pk,
        trip__owner=request.user,
    )

    trip = item.trip
    trip_pk = trip.pk

    if request.method != "POST":
        return redirect("trip_detail", pk=trip_pk)

    item.delete()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        packing_items = trip.packing_items.all()

        return JsonResponse({
            "success": True,
            "packed_items": packing_items.filter(is_packed=True).count(),
            "total_items": packing_items.count(),
        })

    return redirect("trip_detail", pk=trip_pk)
