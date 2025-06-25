import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule, NgIf } from '@angular/common';
import {FormsModule} from '@angular/forms';
import { HttpHeaders } from '@angular/common/http';
import {
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonItem,
  IonLabel,
  IonInput,
  IonTextarea,
  IonButton,
  IonButtons,
  IonBackButton,
  ToastController,
  LoadingController,
} from '@ionic/angular/standalone';

const API_URL = 'http://localhost:8000/post/api/editar/';

@Component({
  selector: 'app-edit-post',
  standalone: true,
  templateUrl: './edit-post.page.html',
  styleUrls: ['./edit-post.page.scss'],
  imports: [
    CommonModule,
    FormsModule,
    HttpClientModule,
    NgIf,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonContent,
    IonItem,
    IonLabel,
    IonInput,
    IonTextarea,
    IonButton,
    IonButtons,
    IonBackButton,
  ],
})
export class EditPostPage implements OnInit {
  postId!: number;
  titulo_post: string = '';
  descricao: string = '';

  constructor(
    private route: ActivatedRoute,
    private http: HttpClient,
    private router: Router,
    private toastCtrl: ToastController,
    private loadingCtrl: LoadingController
  ) {}

  ngOnInit() {
    this.postId = +this.route.snapshot.paramMap.get('id')!;
    this.carregarPost();
  }

  readonly API_GET_URL = 'http://localhost:8000/post/api/post/';

  async carregarPost() {
  const loading = await this.loadingCtrl.create({ message: 'Carregando post...' });
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

  this.http.get<any>(`${this.API_GET_URL}${this.postId}/`,{headers}).subscribe({
    next: (post) => {
      this.titulo_post = post.titulo_post;
      this.descricao = post.descricao;
      loading.dismiss();
    },
    error: async () => {
      loading.dismiss();
      const toast = await this.toastCtrl.create({
        message: 'Erro ao carregar post.',
        duration: 3000,
        color: 'danger',
      });
      toast.present();
      this.router.navigate(['/']);
    },
  });
}

  async salvarPost() {
    const loading = await this.loadingCtrl.create({ message: 'Salvando alterações...' });
    await loading.present();

    const postAtualizado = {
      titulo_post: this.titulo_post,
      descricao: this.descricao,
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

    this.http.put(`${API_URL}${this.postId}/`, postAtualizado,{headers}).subscribe({
      next: async () => {
        loading.dismiss();
        const toast = await this.toastCtrl.create({
          message: 'Post atualizado com sucesso!',
          duration: 2000,
          color: 'success',
        });
        await toast.present();
        this.router.navigate(['/']);
      },
      error: async () => {
        loading.dismiss();
        const toast = await this.toastCtrl.create({
          message: 'Erro ao salvar post.',
          duration: 3000,
          color: 'danger',
        });
        toast.present();
      },
    });
  }
}
