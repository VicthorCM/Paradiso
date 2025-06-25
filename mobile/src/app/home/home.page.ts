import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common'; // ✅ necessário para *ngIf, *ngFor etc.
import { Storage } from '@ionic/storage-angular';
import { CapacitorHttp, HttpOptions, HttpResponse } from '@capacitor/core';
import { AuthService } from '../services/auth.service'; 
import {
  IonContent,
  IonLabel,
  IonList,
  IonItem,
  IonInput,
  IonButton,
  LoadingController,
  NavController,
  AlertController,
  ToastController
} from '@ionic/angular/standalone';
import { Usuario } from './usuario.model';

@Component({
  selector: 'app-home',
  standalone: true, // ✅ importante para standalone components
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  imports: [
    CommonModule, // ✅ necessário para diretivas como *ngIf
    FormsModule,
    IonContent,
    IonLabel,
    IonList,
    IonItem,
    IonInput,
    IonButton
  ],
  providers: [Storage]
})
export class HomePage {
  constructor(
    public controle_carregamento: LoadingController,
    public controle_navegacao: NavController,
    public controle_alerta: AlertController,
    public controle_toast: ToastController,
    public storage: Storage,
    private authService: AuthService,
  ) {}

  public instancia: { username: string; password: string } = {
    username: '',
    password: ''
  };

  async ngOnInit() {
    await this.storage.create();
  }

  async autenticarUsuario() {
    const loading = await this.controle_carregamento.create({
      message: 'Autenticando...',
      duration: 15000
    });
    await loading.present();

    const options: HttpOptions = {
      headers: { 'Content-Type': 'application/json' },
      url: 'http://127.0.0.1:8000/users/api/login/',
      data: this.instancia
    };

    CapacitorHttp.post(options)
      .then(async (resposta: HttpResponse) => {
         if (resposta.status === 200) {
      let usuario: Usuario = Object.assign(new Usuario(), resposta.data);
      await this.storage.set('usuario', usuario);
      console.log('usuario',usuario);
      // 🟢 Salva o ID do usuário logado
      this.authService.login(usuario.id,usuario.token);

      await loading.dismiss();
      this.controle_navegacao.navigateRoot('/post');
    } else {
      loading.dismiss();
      this.apresenta_mensagem(resposta.status);
    }
      })
      .catch(async (erro: any) => {
        console.log(erro);
        loading.dismiss();
        this.apresenta_mensagem(erro?.status);
      });
  }

  async apresenta_mensagem(codigo: number) {
    const mensagem = await this.controle_toast.create({
      message: `Falha ao autenticar usuário: código ${codigo}`,
      cssClass: 'ion-text-center',
      duration: 2000
    });
    mensagem.present();
  }
}
