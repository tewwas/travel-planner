from django import forms

from .models import City, Country, Trip


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip

        fields = [
            "title",
            "country",
            "city",
            "start_date",
            "end_date",
            "budget",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Например, Летняя поездка",
                }
            ),

            "country": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "city": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "start_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "end_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "budget": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Например, 100000",
                    "min": "0",
                    "step": "1000",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["country"].queryset = Country.objects.all()
        self.fields["country"].empty_label = "Выберите страну"

        self.fields["city"].empty_label = "Сначала выберите страну"

        if self.instance and self.instance.pk and self.instance.country_id:
            self.fields["city"].queryset = City.objects.filter(
                country=self.instance.country
            )
            self.fields["city"].empty_label = "Выберите город"
        else:
            self.fields["city"].queryset = City.objects.none()

        if self.is_bound:
            country_id = self.data.get("country")

            if country_id:
                try:
                    country_id = int(country_id)

                    self.fields["city"].queryset = City.objects.filter(
                        country_id=country_id
                    )

                    self.fields["city"].empty_label = "Выберите город"

                except (TypeError, ValueError):
                    self.fields["city"].queryset = City.objects.none()

    def clean(self):
        cleaned_data = super().clean()

        country = cleaned_data.get("country")
        city = cleaned_data.get("city")
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if country and city and city.country_id != country.id:
            self.add_error(
                "city",
                "Выбранный город не относится к выбранной стране.",
            )

        if start_date and end_date and end_date < start_date:
            self.add_error(
                "end_date",
                "Дата окончания не может быть раньше даты начала.",
            )

        return cleaned_data