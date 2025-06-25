from .models import Post
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
# from .forms import VeiculoForm
from django.http import FileResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import ListAPIView, DestroyAPIView,CreateAPIView, UpdateAPIView
# from .serializers import SerializadorVeiculo
from rest_framework. permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import render, get_object_or_404,redirect
from .models import Comentario
from .forms import ComentarioForm
from .serializers import SerializadorComentario
from django.contrib.auth.models import User


class ListarComentarioAPI(ListAPIView):
    serializer_class = SerializadorComentario
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comentario.objects.all()




class CriarComentarioAPIView(CreateAPIView):
    """
    View para criar novos comentários.
    Permite apenas usuários autenticados.
    """
    queryset = Comentario.objects.all()
    serializer_class = SerializadorComentario
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """
        Sobrescreve o método perform_create para definir automaticamente
        o usuário logado como o autor do comentário.
        """
       
        serializer.save(user=User.objects.get(id=self.request.data['user']))
