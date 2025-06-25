from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Comentario, Post
from rest_framework.authtoken.models import Token
from obras.models import *
class ComentarioAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.genero = Genero.objects.create(nome='Ação')
        self.obra = Obra.objects.create(
            titulo='Minha Obra',
            ano_lancamento=2023,
            tipo='FILME',
            genero=self.genero,
            duracao_minutos=120,
            diretor='Diretor Teste'
        )
        self.post = Post.objects.create(
            user=self.user,
            titulo_post='Post teste',
            descricao='Conteúdo do post',
            obra=self.obra
        )
        self.list_url = reverse('listar-api-comentario')  
        self.create_url = reverse('criar-api-comentario')  
        
        
        self.client.force_authenticate(user=self.user)

    def test_listar_comentarios_autenticado(self):
        
        Comentario.objects.create(user=self.user, post=self.post, texto="Comentário 1")
        Comentario.objects.create(user=self.user, post=self.post, texto="Comentário 2")

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['texto'], "Comentário 1")

    def test_listar_comentarios_nao_autenticado(self):
        self.client.force_authenticate(user=None)  # Remove autenticação
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 401)  # Unauthorized

    def test_criar_comentario_com_usuario(self):
        data = {
            'post': self.post.id,
            'texto': 'Comentário criado via API',
            'user': self.user.id  
        }
        response = self.client.post(self.create_url, data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comentario.objects.count(), 1)
        self.assertEqual(Comentario.objects.first().texto, 'Comentário criado via API')
        self.assertEqual(Comentario.objects.first().user, self.user)

    def test_criar_comentario_sem_usuario(self):
        # Se tentar criar sem user, deve dar erro
        data = {
            'post': self.post.id,
            'texto': 'Comentário sem usuário',
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 400)  
