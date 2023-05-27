from django import forms


class DateForm(forms.Form):
    date = forms.DateField(label='Дата', required=False)