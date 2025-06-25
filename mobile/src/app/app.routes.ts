import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'home',
    loadComponent: () => import('./home/home.page').then((m) => m.HomePage),
  },
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full',
  },
  {
    path: 'post',
    loadComponent: () => import('./post/post.page').then( m => m.PostPage)
  },
  {
    path: 'edit-post/:id',
    loadComponent: () => import('./edit-post/edit-post.page').then( m => m.EditPostPage)
  },
  {
    path: 'create-post',
    loadComponent: () => import('./create-post/create-post.page').then( m => m.CreatePostPage)
  },
  {
    path: 'obras',
    loadComponent: () => import('./obras/obras.page').then( m => m.ObrasPage)
  },
];
