
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('listar/',ListarObrasView.as_view(),name='listar-obras'),
    path('cadastrar/',CriarObraView.as_view(),name='cadastrar-obra'),
    path('excluir/<str:pk>/',ExcluirObraView.as_view(),name='excluir-obra'),
    path('editar/<str:pk>/',EditarObraView.as_view(),name='editar-obra'),
    path('detalhes/<str:pk>/',DetalhesObraView.as_view(),name='detalhes-obra'),
    path('api/obras/', ObraListCreateAPIView.as_view(), name='api-obras-list-create'),
    path('api/obras/<int:pk>/', ObraRetrieveUpdateDestroyAPIView.as_view(), name='api-obras-detail'),

]
