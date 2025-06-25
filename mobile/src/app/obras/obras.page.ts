import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule, NgFor, NgIf } from '@angular/common';
import { HttpHeaders } from '@angular/common/http';
import {
  IonContent,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonList,
  IonItem,
  IonLabel,
  IonThumbnail,
  IonImg,
  IonText,
  IonRefresher,
  IonRefresherContent,
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardSubtitle,
  IonCardContent,
  IonButtons,
    IonMenuButton,
     IonFab,
  IonFabButton,
} from '@ionic/angular/standalone';
import { RouterModule } from '@angular/router';

const API_URL = 'http://localhost:8000/obras/api/obras/'; // Ajuste seu endpoint aqui

interface Genero {
  nome: string;
}

interface Obra {
  id: number;
  titulo: string;
  ano_lancamento: number;
  tipo: string;
  genero: Genero | null;
  sinopse?: string;
  poster?: string; // URL da imagem
}

@Component({
  selector: 'app-obras',
  standalone: true,
  templateUrl: './obras.page.html',
  styleUrls: ['./obras.page.scss'],
  imports: [
    HttpClientModule,
    CommonModule,
    NgFor,
    NgIf,
    RouterModule,
    IonContent,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonList,
    IonItem,
    IonLabel,
    IonThumbnail,
    IonImg,
    IonText,
    IonRefresher,
    IonRefresherContent,
    IonCard,
    IonCardHeader,
    IonCardTitle,
    IonCardSubtitle,
    IonCardContent,
    IonMenuButton,
    IonButtons,
      IonFab,
  IonFabButton,
  ],
})
export class ObrasPage implements OnInit {
  obras: Obra[] = [];

  constructor(private http: HttpClient, private cdr: ChangeDetectorRef) {}

  ngOnInit() {
    this.loadObras();
  }

  loadObras() {

    const token = localStorage.getItem('userToken');
  if (!token) {
    console.error('Token não encontrado!');
    return;
  }

  const headers = new HttpHeaders({
    'Authorization': `Token ${token}`
  });

    this.http.get<Obra[]>(API_URL,{headers}).subscribe({
      next: (data) => {
        this.obras = data;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Erro ao carregar obras:', err);
      },
    });
  }

  doRefresh(event: any) {
    this.http.get<Obra[]>(API_URL).subscribe({
      next: (data) => {
        this.obras = data;
        event.target.complete();
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Erro ao atualizar obras:', err);
        event.target.complete();
      },
    });
  }
}
