// src/app/services/auth.service.ts
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private currentUserId: number | null = null;
  private currentUserToken: string | null = null;

  constructor() {
    const storedId = localStorage.getItem('userId');
    this.currentUserId = storedId ? Number(storedId) : null;
  }

  login(userId: number, token: string) {
    this.currentUserId = userId;
    this.currentUserToken = token;
    localStorage.setItem('userId', userId.toString());
    localStorage.setItem('userToken', token);
  }

  getCurrentUserId(): number | null {
    return this.currentUserId;
  }
  getCurrentUserToken(): string | null{
      return this.currentUserToken;
  }

  logout() {
    this.currentUserId = null;
    localStorage.removeItem('userId');
  }
}
