from django.db import models
from .consts import *
class Genero(models.Model):
    nome = models.TextField(max_length=100) 
    
    def __str__(self):
        return f"{self.nome}"

class Obra(models.Model):
    titulo = models.TextField(max_length=200,null=False)
    ano_lancamento = models.PositiveIntegerField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    genero = models.ForeignKey(Genero,on_delete=models.SET_NULL,null=True) 
    sinopse = models.TextField(blank=True, null=True)
    duracao_minutos = models.PositiveIntegerField(blank=True, null=True)  # Para filmes
    numero_temporadas = models.PositiveIntegerField(blank=True, null=True)  # Para séries
    numero_episodios = models.PositiveIntegerField(blank=True, null=True)  # Para séries
    diretor = models.CharField(max_length=100, blank=True, null=True) 
    poster = models.ImageField(blank=True, null= True, upload_to='obras/fotos')
    
    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()})"