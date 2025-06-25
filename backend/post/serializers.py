from rest_framework import serializers
from .models import Post
from comentarios.serializers import *
from obras.models import Obra  
from django.contrib.auth.models import User

class SerializadorPost(serializers.ModelSerializer):
    comentarios = SerializadorComentario(many=True, read_only=True)
    nome_obra = serializers.SerializerMethodField()  
    user_username = serializers.SerializerMethodField()  
    class Meta: 
        model = Post
        fields = ['id', 'user', 'criado', 'titulo_post', 'descricao', 'obra', 'nome_obra', 'comentarios','user_username']

    def get_nome_obra(self, obj):
        return obj.obra.titulo if obj.obra else None
    
    def get_user_username(self, obj):
        return obj.user.username if obj.user else None
