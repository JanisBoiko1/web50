from django.contrib import admin

# Register your models here.
from .models import Entry
from .forms import EntryForm



class EntryAdmin(admin.ModelAdmin):
    list_display=["__str__", "title", "text"] #maybe use __str__ if error/not sure I need this
    form = EntryForm
    # class Meta:
    #   model: Entry
    
admin.site.register(Entry, EntryAdmin)