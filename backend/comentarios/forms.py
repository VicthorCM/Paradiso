from django.forms import ModelForm, TextInput, Select, Textarea
from .models import Comentario

class ComentarioForm(ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escreva seu comentário',
                'rows': 4,
                'required': True
            }),
        }