
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('home/',Home.as_view(),name='home'),
    path('novo/',CriarPostView.as_view(),name='criar-post'),
    path('editar/<str:pk>/',EditarPostView.as_view(),name='editar-post'),
    path('excluir/<str:pk>/',ExcluirPostView.as_view(),name='excluir-post'),
    path('detalhes/<str:pk>/',DetalhesPostView.as_view(),name='detalhes-post'),
    path('api/all/',ListarPostAPI.as_view(),name='listar-api-post'),
    path('api/post/<str:pk>/',GetPostAPI.as_view(),name='get-post-api'),
    path('api/criar/',CriarPostAPI.as_view(),name='criar-api-post'),
    path('api/editar/<str:pk>/',EditarPostAPI.as_view(),name='editar-api-post'),
    path('api/excluir/<str:pk>',ExcluirPostAPI.as_view(),name='excluir-api-post'),
    path('<int:pk>/like/', LikePostView.as_view(), name='like-post'),
]
