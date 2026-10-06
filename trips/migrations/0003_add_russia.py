from django.db import migrations


def add_russia(apps, schema_editor):
    Country = apps.get_model("trips", "Country")
    City = apps.get_model("trips", "City")

    russia, _ = Country.objects.get_or_create(
        name="Россия"
    )

    for city_name in [
        "Москва",
        "Санкт-Петербург",
        "Владивосток",
        "Краснодар",
        "Калининград",
    ]:
        City.objects.get_or_create(
            name=city_name,
            country=russia,
        )


def remove_russia(apps, schema_editor):
    Country = apps.get_model("trips", "Country")
    City = apps.get_model("trips", "City")

    try:
        russia = Country.objects.get(name="Россия")
    except Country.DoesNotExist:
        return

    City.objects.filter(country=russia).delete()
    russia.delete()


class Migration(migrations.Migration):

    dependencies = [
        ("trips", "0002_city_country_alter_trip_options_alter_trip_city_and_more"),
    ]

    operations = [
        migrations.RunPython(
            add_russia,
            remove_russia,
        ),
    ]
