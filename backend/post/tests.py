from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from post.models import Post
from obras.models import Obra, Genero

class PostViewsTestCase(TestCase):
    def setUp(self):
        # Cliente HTTP tradicional
        self.client = Client()

        # Cliente da API com autenticação por Token
        self.api_client = APIClient()

        # Criar usuário
        self.user = User.objects.create_user(username='testeuser', password='123456')

        # Token para o usuário
        self.token = Token.objects.create(user=self.user)
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Criar gênero e obra
        self.genero = Genero.objects.create(nome='Ação')
        self.obra = Obra.objects.create(
            titulo='Filme Teste',
            ano_lancamento=2024,
            tipo='FILME',  # deve estar entre os valores de TIPO_CHOICES
            genero=self.genero,
            sinopse='Teste',
            duracao_minutos=120
        )

        # Criar post
        self.post = Post.objects.create(
            titulo_post='Post de teste',
            descricao='Descrição do post',
            user=self.user,
            obra=self.obra
        )

    def test_home_view_autenticado(self):
        self.client.login(username='testeuser', password='123456')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Post de teste')

    def test_home_view_nao_autenticado(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)  # Redireciona para login

    def test_criar_post_view(self):
        self.client.login(username='testeuser', password='123456')
        url = reverse('criar-post')
        data = {
            'titulo_post': 'Novo post view',
            'descricao': 'Descrição nova',
            'obra': self.obra.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redireciona após sucesso
        self.assertEqual(Post.objects.count(), 2)

    def test_criar_post_api(self):
        url = reverse('criar-api-post')
        data = {
            'titulo_post': 'Post via API',
            'descricao': 'Conteúdo do post',
            'user': self.user.id,
            'obra': self.obra.id
        }
        response = self.api_client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), 2)

    def test_get_post_api(self):
        url = reverse('get-post-api', kwargs={'pk': self.post.id})
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['titulo_post'], self.post.titulo_post)

    def test_editar_post_api(self):
        url = reverse('editar-api-post', kwargs={'pk': self.post.id})
        data = {
            'titulo_post': 'Título editado',
            'descricao': 'Nova descrição',
            'user': self.user.id,
            'obra': self.obra.id
        }
        response = self.api_client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        self.assertEqual(self.post.titulo_post, 'Título editado')

    def test_excluir_post_api(self):
        url = reverse('excluir-api-post', kwargs={'pk': self.post.id})
        response = self.api_client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_like_post_view(self):
        self.client.login(username='testeuser', password='123456')
        url = reverse('like-post', kwargs={'pk': self.post.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.post.likes.filter(id=self.user.id).exists())

    def test_detalhes_post_view_get(self):
        self.client.login(username='testeuser', password='123456')
        url = reverse('detalhes-post', kwargs={'pk': self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sem descrição')


    def test_listar_post_api(self):
        url = reverse('listar-api-post')
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) >= 1)
