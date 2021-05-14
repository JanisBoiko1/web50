from django import forms
from django.forms import ModelForm, Textarea

from .models import Entry

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields =['title','text']
       
class Query(forms.Form):
    title = forms.CharField(required="True", widget=forms.TextInput(attrs={'size': 15}))
    
    
    
    