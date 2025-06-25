export class Usuario
{
  public id: number;
  public username: string;
  public email: string;
  public token: string;

  constructor() { 
    this.id = 0;
    this.username = '';
    this.email = '';
    this.token = '';
  }
}