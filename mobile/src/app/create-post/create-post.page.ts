import { Component } from '@angular/core';
import { CommonModule, NgIf } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { AuthService } from '../services/auth.service'; // ajuste o caminho
import { OnInit } from '@angular/core';
import { HttpHeaders } from '@angular/common/http';
import {
  IonContent,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonItem,
  IonLabel,
  IonInput,
  IonTextarea,
  IonButton,
  IonButtons,
  IonBackButton,
  ToastController,
  LoadingController,
  NavController,
   IonSelect,
  IonSelectOption,
} from '@ionic/angular/standalone';

const API_URL = 'http://localhost:8000/post/api/criar/'; // ajuste para sua API

@Component({
  selector: 'app-create-post',
  standalone: true,
  templateUrl: './create-post.page.html',
  styleUrls: ['./create-post.page.scss'],
  imports: [
    CommonModule,
    FormsModule,
    HttpClientModule,
    NgIf,
    IonContent,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonItem,
    IonLabel,
    IonInput,
    IonTextarea,
    IonButton,
    IonButtons,
    IonBackButton,
    IonSelect,
    IonSelectOption,
   
  ],
})
export class CreatePostPage implements OnInit {
  titulo_post: string = '';
  descricao: string = '';
  currentUserId: number | null = null;
  obraSelecionada: number | null = null;
  obras: any[] = [];

  constructor(
    private http: HttpClient,
    private toastCtrl: ToastController,
    private loadingCtrl: LoadingController,
    private navCtrl: NavController,
    private authService: AuthService,
  ) {}

  ngOnInit() {
    this.currentUserId = this.authService.getCurrentUserId();
    this.carregarObras();
  }

  carregarObras() {
    const token = localStorage.getItem('userToken');

  const headers = new HttpHeaders({
    'Authorization': `Token ${token}`
  });
    this.http.get<any[]>('http://localhost:8000/obras/api/obras/',{headers}).subscribe({
      next: (dados) => {
        this.obras = dados;
      },
      error: (err) => {
        console.error('Erro ao carregar obras:', err);
      }
    });
  }

  async salvarPost() {
    if (!this.titulo_post.trim() || !this.descricao.trim() || !this.obraSelecionada) {
      const toast = await this.toastCtrl.create({
        message: 'Preencha todos os campos e selecione uma obra!',
        duration: 2000,
        color: 'warning',
      });
      toast.present();
      return;
    }

    const loading = await this.loadingCtrl.create({
      message: 'Salvando post...',
    });
    await loading.present();
    console.log(this.obraSelecionada);
    const novoPost = {
      titulo_post: this.titulo_post,
      descricao: this.descricao,
      user: this.currentUserId,
      obra: this.obraSelecionada,
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

    this.http.post(API_URL, novoPost,{headers}).subscribe({
      next: async () => {
        await loading.dismiss();
        const toast = await this.toastCtrl.create({
          message: 'Post criado com sucesso!',
          duration: 2000,
          color: 'success',
        });
        await toast.present();
        this.navCtrl.navigateRoot(['/']);
      },
      error: async (err) => {
        console.error('Erro ao criar post:', err);
        await loading.dismiss();
        const toast = await this.toastCtrl.create({
          message: 'Erro ao criar post.',
          duration: 3000,
          color: 'danger',
        });
        toast.present();
      },
    });
  }
}