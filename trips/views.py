from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TripForm
from .models import City, PackingItem, Trip


def trip_list(request):
    trips = Trip.objects.all()

    return render(
        request,
        "trips/trip_list.html",
        {
            "trips": trips,
        },
    )


def trip_detail(request, pk):
    trip = get_object_or_404(
        Trip,
        pk=pk,
    )

    packing_items = trip.packing_items.all()

    total_items = packing_items.count()
    packed_items = packing_items.filter(
        is_packed=True
    ).count()

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


def trip_create(request):
    if request.method == "POST":
        form = TripForm(request.POST)

        if form.is_valid():
            trip = form.save()

            messages.success(
                request,
                "Поездка успешно создана.",
            )

            return redirect(
                "trip_detail",
                pk=trip.pk,
            )

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


def trip_update(request, pk):
    trip = get_object_or_404(
        Trip,
        pk=pk,
    )

    if request.method == "POST":
        form = TripForm(
            request.POST,
            instance=trip,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Поездка успешно изменена.",
            )

            return redirect(
                "trip_detail",
                pk=trip.pk,
            )

    else:
        form = TripForm(
            instance=trip,
        )

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


def trip_delete(request, pk):
    trip = get_object_or_404(
        Trip,
        pk=pk,
    )

    if request.method == "POST":
        trip.delete()

        messages.success(
            request,
            "Поездка удалена.",
        )

        return redirect("trip_list")

    return render(
        request,
        "trips/trip_confirm_delete.html",
        {
            "trip": trip,
        },
    )


def cities_by_country(request):
    country_id = request.GET.get("country_id")

    if not country_id:
        return JsonResponse(
            {
                "cities": [],
            }
        )

    cities = City.objects.filter(
        country_id=country_id
    ).values(
        "id",
        "name",
    )

    return JsonResponse(
        {
            "cities": list(cities),
        }
    )


def packing_item_add(request, pk):
    trip = get_object_or_404(
        Trip,
        pk=pk,
    )

    if request.method == "POST":
        name = request.POST.get("name", "").strip()

        if name:
            PackingItem.objects.create(
                trip=trip,
                name=name,
            )

        return redirect(
            "trip_detail",
            pk=trip.pk,
        )

    return redirect(
        "trip_detail",
        pk=trip.pk,
    )


def packing_item_toggle(request, pk):
    item = get_object_or_404(
        PackingItem,
        pk=pk,
    )

    item.is_packed = not item.is_packed
    item.save(update_fields=["is_packed"])

    return redirect(
        "trip_detail",
        pk=item.trip.pk,
    )


def packing_item_delete(request, pk):
    item = get_object_or_404(
        PackingItem,
        pk=pk,
    )

    trip_pk = item.trip.pk

    item.delete()

    return redirect(
        "trip_detail",
        pk=trip_pk,
    )