from django.db import models


class Country(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Страна",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="cities",
        verbose_name="Страна",
    )

    name = models.CharField(
        max_length=100,
        verbose_name="Город",
    )

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["country", "name"],
                name="unique_city_per_country",
            ),
        ]
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def __str__(self):
        return self.name


class Trip(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название поездки",
    )

    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        related_name="trips",
        verbose_name="Страна",
    )

    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        related_name="trips",
        verbose_name="Город",
    )

    start_date = models.DateField(
        verbose_name="Дата начала",
    )

    end_date = models.DateField(
        verbose_name="Дата окончания",
    )

    budget = models.IntegerField(
        default=0,
        verbose_name="Бюджет",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    class Meta:
        ordering = ["start_date"]
        verbose_name = "Поездка"
        verbose_name_plural = "Поездки"

    def __str__(self):
        return self.title

    @property
    def duration_days(self):
        return (self.end_date - self.start_date).days + 1

    @property
    def trip_status(self):
        from datetime import date

        today = date.today()

        if today < self.start_date:
            days_left = (self.start_date - today).days

            if days_left == 1:
                return "Завтра"

            return f"Через {days_left} дней"

        if today > self.end_date:
            return "Поездка закончена"

        current_day = (today - self.start_date).days + 1

        return f"День {current_day} из {self.duration_days}"


class PackingItem(models.Model):
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="packing_items",
        verbose_name="Поездка",
    )

    name = models.CharField(
        max_length=150,
        verbose_name="Вещь",
    )

    is_packed = models.BooleanField(
        default=False,
        verbose_name="Собрано",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["is_packed", "created_at", "id"]
        verbose_name = "Вещь"
        verbose_name_plural = "Вещи"

    def __str__(self):
        return self.name