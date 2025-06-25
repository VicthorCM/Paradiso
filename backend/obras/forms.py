
from django.forms import ModelForm, TextInput, NumberInput, Select, Textarea
from .models import Obra

class ObraForm(ModelForm):
    class Meta:
        model = Obra
        fields = ['titulo', 'ano_lancamento', 'tipo', 'genero', 'sinopse', 'diretor', 'duracao_minutos', 'numero_temporadas', 'numero_episodios','poster']
        widgets = {
            'titulo': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o título da obra',
                'required': True
            }),
            'ano_lancamento': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 2023',
                'min': 1888,  # Primeiro filme conhecido
                'max': 2100,  # Limite futuro razoável
                'required': True
            }),
            'tipo': Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'genero': Select(attrs={
                'class': 'form-select',
            }),
            'sinopse': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descreva a sinopse da obra',
                'rows': 5
            }),
            'diretor': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do diretor',
            }),
            'duracao_minutos': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Duração em minutos',
                'min': 1,
                'required': False
            }),
            'numero_temporadas': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de temporadas',
                'min': 1,
                'required': False
            }),
            'numero_episodios': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de episódios',
                'min': 1,
                'required': False
            }),
        }
