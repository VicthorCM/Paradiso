import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule, DatePipe, NgIf, NgFor } from '@angular/common';
import { add, pencilOutline, trashOutline, eyeOutline, send } from 'ionicons/icons'; 
import { AuthService } from '../services/auth.service';
import { FormsModule } from '@angular/forms'; 
import { HttpHeaders } from '@angular/common/http';

import {
  IonContent,
  IonHeader,
  IonMenuButton,
  IonToolbar,
  IonTitle,
  IonList,
  IonItem,
  IonLabel,
  IonText,
  IonButtons,
  IonButton,
  IonIcon,
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardSubtitle,
  IonCardContent,
  IonRefresher,
  IonRefresherContent,
  LoadingController,
  ToastController,
  NavController,
  IonFab,
  IonFabButton,
  IonInput, 
} from '@ionic/angular/standalone';

const API_URL_POSTS = 'http://localhost:8000/post/api/all/'; 
const API_URL_COMMENTS = 'http://localhost:8000/comentarios/api/'; 

interface UserDetails {
  id: number;
  username: string;
}

interface Comment {
  id?: number; 
  post: number;
  user: UserDetails; 
  texto: string;
  criado: string;
}

interface Post {
  id?: number;
  titulo_post: string;
  descricao: string;
  criado: string;
  user: number; 
  obra: string;
  nome_obra: string;
  user_username: string; 
  comentarios: Comment[];
}

@Component({
  selector: 'app-post',
  standalone: true,
  templateUrl: './post.page.html',
  styleUrls: ['./post.page.scss'],
  imports: [
    HttpClientModule,
    CommonModule,
    NgIf,
    NgFor,
    DatePipe,
    FormsModule,
    IonMenuButton,
    IonContent,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonList,
    IonItem,
    IonLabel,
    IonText,
    IonButton,
    IonIcon,
    IonCard,
    IonCardHeader,
    IonCardTitle,
    IonCardSubtitle,
    IonCardContent,
    IonRefresher,
    IonRefresherContent,
    IonFab,
    IonFabButton,
    IonButtons,
    IonInput,
  ],
})
export class PostPage implements OnInit {
  add = add;
  pencilOutline = pencilOutline;
  trashOutline = trashOutline;
  eyeOutline = eyeOutline;
  send = send; 

  posts: Post[] = [];

  currentUserId: number | null = null;
  newCommentText: { [postId: number]: string } = {};

  constructor(
    private http: HttpClient,
    private cdr: ChangeDetectorRef,
    public loadingCtrl: LoadingController,
    public toastCtrl: ToastController,
    private navCtrl: NavController,
    private authService: AuthService,
  ) {}

  ngOnInit() {
    this.currentUserId = this.authService.getCurrentUserId();
    console.log('Current User ID:', this.currentUserId);
    this.loadPosts();
  }

  async loadPosts() {
  const loading = await this.loadingCtrl.create({
    message: 'Carregando publicações...',
  });
  await loading.present();

  const token = localStorage.getItem('userToken');
  if (!token) {
    console.error('Token não encontrado!');
    loading.dismiss();
    return;
  }

  const headers = new HttpHeaders({
    'Authorization': `Token ${token}`
  });

  this.http.get<Post[]>(API_URL_POSTS, { headers }).subscribe({
    next: async (data) => {
      this.posts = data.map((post) => ({
        ...post,
        comentarios: post.comentarios || [],
        user: Number(post.user),
        user_username: post.user_username || 'Desconhecido'
      }));

      this.posts.forEach(post => {
        if (post.id) {
          this.newCommentText[post.id] = '';
        }
      });

      console.log('Posts carregados:', this.posts);
      loading.dismiss();
      this.cdr.detectChanges();
    },
    error: async (err) => {
      console.error('Erro ao carregar posts:', err);
      loading.dismiss();
      const toast = await this.toastCtrl.create({
        message: 'Erro ao carregar posts.',
        duration: 3000,
        color: 'danger',
      });
      toast.present();
    },
  });
}


  async doRefresh(event: any) {
    this.http.get<Post[]>(API_URL_POSTS).subscribe({
      next: (data) => {
        this.posts = data.map(post => ({
            ...post,
            comentarios: post.comentarios || [],
            user: Number(post.user),
            user_username: post.user_username || 'Desconhecido'
        }));
       
        this.posts.forEach(post => {
            if (post.id) {
                this.newCommentText[post.id] = '';
            }
        });
        event.target.complete();
        this.cdr.detectChanges();
      },
      error: async (err) => {
        console.error('Erro ao atualizar posts:', err);
        event.target.complete();
        const toast = await this.toastCtrl.create({
          message: 'Erro ao atualizar posts.',
          duration: 3000,
          color: 'danger',
        });
        toast.present();
      },
    });
  }

  // --- Funções de Comentário ---
  async addComment(postId: number, commentText: string) {
    if (!commentText || commentText.trim() === '') {
      const toast = await this.toastCtrl.create({
        message: 'O comentário não pode estar vazio.',
        duration: 2000,
        color: 'warning',
      });
      toast.present();
      return;
    }

    if (this.currentUserId === null) {
      const toast = await this.toastCtrl.create({
        message: 'Você precisa estar logado para comentar.',
        duration: 2000,
        color: 'warning',
      });
      toast.present();
      return;
    }

    const loading = await this.loadingCtrl.create({
      message: 'Adicionando comentário...',
    });
    await loading.present();

    const commentPayload = {
      post: postId,
      texto: commentText.trim(),
      user:this.currentUserId,
      // 'criado' será automaticamente definido pelo backend
    };

    const token = localStorage.getItem('userToken');
  if (!token) {
    console.error('Token não encontrado!');
    loading.dismiss();
    return;
  }

  const headers = new HttpHeaders({
    'Authorization': `Token ${token}`
  });

    this.http.post<Comment>(API_URL_COMMENTS+'criar/', commentPayload,{headers}).subscribe({
      next: async (newComment) => {
        loading.dismiss();
        const toast = await this.toastCtrl.create({
          message: 'Comentário adicionado com sucesso!',
          duration: 2000,
          color: 'success',
        });
        toast.present();

       
        const postIndex = this.posts.findIndex(p => p.id === postId);
        if (postIndex > -1) {
          
          if (!this.posts[postIndex].comentarios) {
            this.posts[postIndex].comentarios = [];
          }
          
          this.posts[postIndex].comentarios.push(newComment);
      
          this.newCommentText[postId] = '';
          this.cdr.detectChanges(); 
        }
      },
      error: async (err) => {
        console.error('Erro ao adicionar comentário:', err);
        loading.dismiss();
        const toast = await this.toastCtrl.create({
          message: 'Erro ao adicionar comentário. Tente novamente.',
          duration: 3000,
          color: 'danger',
        });
        toast.present();
      },
    });
  }

  // --- Funções de Post (já existentes) ---
  editarPost(post: Post) {
    if (!post.id) {
      console.warn('ID do post é inválido!');
      return;
    }
    this.navCtrl.navigateRoot(['/edit-post', post.id]);
  }

  excluirPost(post: Post) {
    if (!post.id) {
      console.warn('ID do post é inválido!');
      return;
    }
   
    console.log('Excluir post', post.id);
  
  }

  verDetalhes(post: Post) {
    console.log('Ver detalhes do post', post.id);
   
  }

  criarPost() {
    this.navCtrl.navigateRoot(['/create-post']);
  }
}