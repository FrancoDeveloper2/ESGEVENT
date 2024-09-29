from django import forms

class ProductoSearchForm(forms.Form):
    query = forms.CharField(label='Buscar producto', max_length=100)
