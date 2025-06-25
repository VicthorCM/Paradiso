from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from post.models import Post

class Comentario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post,null=False, on_delete=models.CASCADE,related_name='comentarios')
    texto = models.TextField(max_length=500)
    criado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário por {self.user.username} em {self.post}"
    
