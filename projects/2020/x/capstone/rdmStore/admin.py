from django.contrib import admin
from .models import User, Endereco, Categoria, Item, Compras, Feedbacks

# Register your models here.

admin.site.register(User)
admin.site.register(Endereco)
admin.site.register(Categoria)
admin.site.register(Item)
admin.site.register(Compras)
admin.site.register(Feedbacks)