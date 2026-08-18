from django import forms

from .models import Trip


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
                    "placeholder": "Например: Путешествие в Италию",
                }
            ),

            "country": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Например: Италия",
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Например: Рим",
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
                    "placeholder": "Например: 100000",
                    "min": "0",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError(
                    "Дата окончания не может быть раньше даты начала."
                )

        return cleaned_data