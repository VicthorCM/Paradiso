
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
   
    path('api/all/',ListarComentarioAPI.as_view(),name='listar-api-comentario'),
    path('api/criar/',CriarComentarioAPIView.as_view(),name='criar-api-comentario'),

]
