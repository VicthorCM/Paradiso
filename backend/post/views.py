from .models import Post
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
# from .forms import VeiculoForm
from django.http import FileResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import ListAPIView, DestroyAPIView,CreateAPIView, UpdateAPIView, RetrieveAPIView
# from .serializers import SerializadorVeiculo
from rest_framework. permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from .forms import PostForm
from django.shortcuts import render, get_object_or_404,redirect
from comentarios.models import Comentario
from comentarios.forms import ComentarioForm
from .serializers import SerializadorPost
from .permissions import IsPostAutor
from django.db.models import Q
from django.http import JsonResponse

class Home(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'post/home.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '')
        if query:
            queryset = queryset.filter(
                Q(titulo_post__icontains=query) |
                Q(descricao__icontains=query) 
              
            ).select_related('user').prefetch_related('likes') 
        return queryset.order_by('-criado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['recent_comments'] = Comentario.objects.select_related('user', 'post').order_by('-criado')[:5]
        for post in context['posts']:
            post.is_liked_by_user = post.likes.filter(id=self.request.user.id).exists()
        return context

class LikePostView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        return JsonResponse({
            'liked': liked,
            'likes_count': post.likes.count()
        })

class ListarPostAPI(ListAPIView):
    serializer_class = SerializadorPost
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Post.objects.all().prefetch_related('comentarios')

class CriarPostView(LoginRequiredMixin,CreateView):
    model = Post
    form_class = PostForm
    context_object_name = 'post'
    template_name = 'post/cadastrar.html'
    success_url = reverse_lazy('home') 

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return super().form_valid(form)

class CriarPostAPI(CreateAPIView):
    serializer_class = SerializadorPost
    queryset = Post.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes =  [IsAuthenticated]

class GetPostAPI(RetrieveAPIView):
    serializer_class = SerializadorPost
    queryset = Post.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes =  [IsAuthenticated]
        
class EditarPostView(LoginRequiredMixin,UpdateView):
    model = Post
    form_class =PostForm
    context_object_name = 'post'
    template_name = 'post/cadastrar.html'
    success_url = reverse_lazy('home') 

class EditarPostAPI(UpdateAPIView):
    queryset = Post.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,IsPostAutor]
    serializer_class = SerializadorPost

class ExcluirPostView(LoginRequiredMixin,DeleteView):
    model = Post
    context_object_name = 'post'
    template_name = 'alert.html'
    success_url = reverse_lazy('home') 

class ExcluirPostAPI(DestroyAPIView):
    queryset = Post.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,IsPostAutor]



class DetalhesPostView(View):
    
    def get(self,request,pk):
        context={}
        post = Post.objects.get(id=pk)
        comentarios = Comentario.objects.filter(post=post)
        form = ComentarioForm()
        context['comentarios'] = comentarios
        context['post'] = post
        context['form'] = form
        return render(request,'post/detalhes.html',context)
    
    def post(self,request,pk):
        post = get_object_or_404(Post, id=pk)
        form = ComentarioForm(request.POST)
        
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.post = post
            comentario.user = request.user  # se tiver autenticação
            comentario.save()
            return redirect('detalhes-post', pk=pk)
        
        # Se inválido, renderiza novamente com erros
        comentarios = Comentario.objects.filter(post=post)
        context = {
            'post': post,
            'comentarios': comentarios,
            'form': form
        }
        return render(request, 'post/detalhes.html', context)



