from django.db import models
from django.contrib.auth.models import User
from obras.models import Obra
from django.conf import settings

class Post(models.Model):
    user = models.ForeignKey(User,null=False, on_delete= models.CASCADE)
    criado = models.DateTimeField(auto_now_add=True)
    titulo_post = models.TextField(null=False,max_length=200)
    descricao = models.TextField(blank=True,max_length=500)
    obra = models.ForeignKey(Obra,null=False,on_delete=models.DO_NOTHING)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)  

    @property
    def likes_count(self):
        return self.likes.count()
    
    def __str__(self):
        return super().__str__()