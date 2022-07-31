from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Endereco(models.Model):
    cpf = models.CharField(max_length=11, blank=True)
    telefone = models.CharField(max_length=15, blank=True)
    nomeCompleto = models.CharField(max_length=2200, blank=True)
    cep = models.CharField(max_length=8, blank=True)
    rua = models.CharField(max_length=200, blank=True)
    numero = models.IntegerField(blank=True)
    informacoes_adicionais = models.CharField(max_length = 2200, blank=True)
    complemento = models.CharField(max_length = 2200, blank=True)
    endereco_usuario = models.ForeignKey(User, default=0, on_delete=models.CASCADE, related_name="compra_usuario")
    
    
    def __str__ (self):
        return f"{self.rua}, {self.numero}, {self.cep}."
        
class Categoria(models.Model):
    categoria = models.CharField(max_length=100)
    
    def __str__ (self):
        return f"{self.categoria}."

class Item(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length = 2200, null=True)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    tipo = models.CharField(max_length = 100, null=True)
    tamanho = models.CharField(max_length = 20)
    imagem = models.ImageField(null=True)
    item_categoria = models.ForeignKey(Categoria, default=0, on_delete=models.CASCADE, related_name="itemCategoria")
    promocao = models.BooleanField(null=True)
    disponivel = models.BooleanField(null=True)
    destaque = models.BooleanField(null=True)
    timestanp = models.DateTimeField(auto_now_add=True, auto_now=False)
    watchers = models.ManyToManyField(User,  default=[0], null=True, related_name="watchedListing")
    
    def serialize(self):
        return {
            "nome": self.nome,
            "descricao": self.descricao,
            "preco": self.preco,
            "tamanho":self.tamanho,
            "imagem": self.imagem,
            "user":self.user.id,
            "item_categoria": self.item_categoria,
            "promocao": self.promocao,
            "disponivel": self.disponivel,
            "destaque": self.destaque,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "watchers": [user.username for user in self.watchers.all()],
        }
    
class Compras(models.Model):
    total = models.DecimalField(max_digits=6, decimal_places=2)
    frete = models.DecimalField(max_digits=6, decimal_places=2)
    desconto = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    compra_usuario = models.ForeignKey(User, default=0, on_delete=models.CASCADE, related_name="endereco_usuario")
    compra_itens = models.ManyToManyField(Item,  default=[0], null=True, related_name="comentario_item")
    compra_endereco = models.ForeignKey(Endereco, default=0, on_delete=models.SET_DEFAULT)
    
    def __str__ (self):
        return f"{self.total}"

class Feedbacks(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    comentario_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comentario = models.CharField(max_length = 2200, null=True)
    
    def __str__ (self):
        return f"{self.item_id}. {self.comentario_user} comentou: {self.comentario}."

