from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TripForm
from .models import City, Trip


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

    return render(
        request,
        "trips/trip_detail.html",
        {
            "trip": trip,
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