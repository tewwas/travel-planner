from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.trip_list,
        name="trip_list"
    ),

    path(
        "trips/<int:pk>/",
        views.trip_detail,
        name="trip_detail"
    ),

    path(
        "trips/create/",
        views.trip_create,
        name="trip_create"
    ),

    path(
        "trips/<int:pk>/edit/",
        views.trip_update,
        name="trip_update"
    ),

    path(
        "trips/<int:pk>/delete/",
        views.trip_delete,
        name="trip_delete"
    ),
]