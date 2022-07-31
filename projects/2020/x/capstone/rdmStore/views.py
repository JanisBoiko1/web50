from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404

from .models import User, Item, Categoria


# Create your views here.

#index pode ir para  apagina inicial e apresentar o layout e os links para outros ambientes 
def index(request):
    #select categorias
    categorias = Categoria.objects.all()
    print(categorias)
        
    #select destaques
    items_destaque = Item.objects.filter(destaque=True)
    
    #select recentes
    #https://stackoverflow.com/questions/20555673/django-query-get-last-n-records
    items_recentes = Item.objects.order_by('-timestanp')[:6]
    
    #select promoções
    items_promocionais = Item.objects.filter(promocao=True)

    return render(request, "rdmStore/index.html", {
        "items_destaque": items_destaque,
        "items_recentes": items_recentes, 
        "items_promocionais": items_promocionais,
        "categorias": categorias,
    })


def new(request):
    return render(request, "rdmStore/new.html")

def login_view(request):
    #select categorias
    categorias = Categoria.objects.all()
    
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "rdmStore/login.html", {
                "message": "Invalid username and/or password.",
                "categorias": categorias,
            })
    else:
        return render(request, "rdmStore/login.html", {
            "categorias": categorias,
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    #select categorias
    categorias = Categoria.objects.all()
    
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "rdmStore/register.html", {
                "message": "Passwords must match.",
                "categorias": categorias,
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "rdmStore/register.html", {
                "message": "Username already taken.",
                "categorias": categorias,
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "rdmStore/register.html", {
            "categorias": categorias,
        })

#barrinha de pesquisa
#categorias-mostrar
def selecao(request, elemento):
    
    #select categorias
    categorias = Categoria.objects.all()
    
    nome_categoria =""
    items_categoria = []
    
    for categoria in categorias:
        if str(categoria) == (elemento + "."):
            items_categoria = Item.objects.filter(item_categoria=categoria)
            # print(items_categoria)
            nome_categoria = elemento
    
    #search
    #check if parameter element is similar to name, description or size (Item.nome, .descricao and . tamanho)
    if nome_categoria == "":
         #get all items
         items_all = Item.objects.all()
         
         #iterate through them and compare strings
         for items in items_all:
             
             if((elemento.upper() in items.nome.upper()) or (elemento.upper() in items.descricao.upper()) or (elemento.upper() in items.tamanho.upper())):
                 #if similar, filter by id and add to variable items_categoria
                 items_categoria += Item.objects.filter(id = items.id)
         
         

    return render(request, "rdmStore/categoriasEBusca.html",{
        "categorias": categorias,
        "items_categoria": items_categoria,
        "categoria_nome" : nome_categoria,
    })


#itens-mostrar

#itens-editar

#itens-carrinho

#comparar

#acessar perfil de usuario

#acessar compra antiga

#acessar perfil da empresa

#reclamações e pedidos de devolução

#politica de trocas da empresa
