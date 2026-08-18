from django.contrib import admin

from .models import Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "country",
        "city",
        "start_date",
        "end_date",
        "budget",
        "created_at",
    )

    list_filter = (
        "country",
        "start_date",
        "end_date",
    )

    search_fields = (
        "title",
        "country",
        "city",
    )