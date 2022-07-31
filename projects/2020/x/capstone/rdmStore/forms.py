from django import forms
from .models import Item

#search form
class ItemSearchForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['nome']
        labels = {
            "nome": ""
        }


        