from django import forms

class DatePlaciUpdateForm(forms.Form):
    cod_placa = forms.CharField(label = 'cod_placa', max_length=100)
    min_placa = forms.CharField(label = 'min_placa', max_length=100)
    multiplication_factor = forms.CharField(label = 'multiplication_factor', max_length=100)