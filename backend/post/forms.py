
from django.forms import ModelForm, TextInput, Select, Textarea
from .models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['titulo_post', 'obra', 'descricao']
        widgets = {
            'titulo_post': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o título do post',
                'required': True
            }),
            'obra': Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'descricao': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escreva sua descrição ou comentário sobre a obra',
                'rows': 5,
                'required': True
            }),
        }

