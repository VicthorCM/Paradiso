from .models import Obra, Genero
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.http import FileResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework. permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .forms import ObraForm
from django.http import FileResponse, Http404
from django.conf import settings
from django.shortcuts import render, get_object_or_404,redirect
import os


# Create your views here.
class ListarObrasView(LoginRequiredMixin,ListView):
    model = Obra
    context_object_name = 'obras'
    template_name = 'obras/listar.html'


class CriarObraView(LoginRequiredMixin,CreateView):
    model = Obra
    form_class = ObraForm
    template_name = 'obras/cadastrar.html'
    success_url = reverse_lazy('listar-obras')

    def form_valid(self, form):

        return super().form_valid(form)

class EditarObraView(LoginRequiredMixin,UpdateView):
    model = Obra
    form_class =ObraForm
    context_object_name = 'obras'
    template_name = 'obras/cadastrar.html'
    success_url = reverse_lazy('listar-obras') 


class ExcluirObraView(LoginRequiredMixin,DeleteView):
    model = Obra
    context_object_name = 'obras'
    template_name = 'alert.html'
    success_url = reverse_lazy('listar-obras') 


class DetalhesObraView(View):
    
    def get(self,request,pk):
        context={}
        obra = Obra.objects.get(id=pk)
        context['obra'] = obra
        return render(request,'obras/detalhes.html',context)
    



class PosterObra(View):
    def get(self, request, arquivo):
        caminho_arquivo = os.path.join(settings.MEDIA_ROOT, 'obras', 'fotos', arquivo)
        
        if os.path.exists(caminho_arquivo):
            return FileResponse(open(caminho_arquivo, 'rb'), content_type='image/jpeg')
        else:
            raise Http404("Poster não encontrado")


from rest_framework import generics, permissions, authentication
from .models import Obra
from .serializers import ObraSerializer

class ObraListCreateAPIView(generics.ListCreateAPIView):
    queryset = Obra.objects.all()
    serializer_class = ObraSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
       
        serializer.save()


class ObraRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Obra.objects.all()
    serializer_class = ObraSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
