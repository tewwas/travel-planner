from django.db import models


class Trip(models.Model):

    title = models.CharField(
        max_length=100,
        verbose_name="Название поездки"
    )

    country = models.CharField(
        max_length=100,
        verbose_name="Страна"
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Город"
    )

    start_date = models.DateField(
        verbose_name="Дата начала"
    )

    end_date = models.DateField(
        verbose_name="Дата окончания"
    )

    budget = models.IntegerField(
        default=0,
        verbose_name="Бюджет"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        ordering = ["-start_date"]
        verbose_name = "Поездка"
        verbose_name_plural = "Поездки"

    def __str__(self):
        return self.title