from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Obra, Genero
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

class ObraViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.genero = Genero.objects.create(nome='Ação')
        self.obra = Obra.objects.create(
            titulo='Obra Existente',
            ano_lancamento=2023,
            tipo='FILME',
            genero=self.genero,
            duracao_minutos=100,
            poster=SimpleUploadedFile(
                name='test_poster.jpg',
                content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF\x21\xF9\x04\x01\x00\x00\x00\x00\x2C\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4C\x01\x00\x3B',
                content_type='image/jpeg'
            )
        )
        self.client.login(username='testuser', password='12345')

    def test_criar_obra_view(self):
        url = reverse('cadastrar-obra')
        image = SimpleUploadedFile(
            name='test_poster.jpg',
            content=b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF!'
                    b'\xF9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01'
                    b'\x00\x00\x02\x02L\x01\x00;',
            content_type='image/gif'
        )
        data = {
            'titulo': 'Nova Obra',
            'ano_lancamento': 2024,
            'tipo': 'FILME',  # atenção ao valor exato
            'genero': self.genero.id,
            'duracao_minutos': 120,
            'poster': image,
        }
        response = self.client.post(url, data)  # sem follow=True
        print(response.status_code)
        print(response.templates)
        if response.status_code != 302:  # se não foi redirecionado, form tem erro
            if hasattr(response, 'context') and 'form' in response.context:
                print(response.context['form'].errors)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Obra.objects.filter(titulo='Nova Obra').exists())


    def test_editar_obra_view(self):
        url = reverse('editar-obra', kwargs={'pk': self.obra.id})
        data = {
            'titulo': 'Obra Editada',
            'ano_lancamento': 2023,
            'tipo': 'FILME',
            'genero': self.genero.id,
            'duracao_minutos': 110,
        }
        response = self.client.post(url, data)
        print(response.status_code)
        if response.status_code != 302:
            if hasattr(response, 'context') and 'form' in response.context:
                print(response.context['form'].errors)
        self.assertEqual(response.status_code, 302)
        self.obra.refresh_from_db()
        self.assertEqual(self.obra.titulo, 'Obra Editada')

