import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { inject } from '@angular/core';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor() { }
  httpClient = inject(HttpClient);
  baseUrl = 'http://localhost:5003';

  signup(data: any) {
    return this.httpClient.post(`${this.baseUrl}/signup`, data);
  }

  login(username: string, password: string) {
    const basicAuth = 'Basic ' + btoa(`${username}:${password}`);

    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': basicAuth
    });

    return this.httpClient.post(`${this.baseUrl}/login`,{}, { headers })
      .pipe(tap((result) => {

        console.log(JSON.stringify(result));
        localStorage.setItem('authUser', JSON.stringify(result));
      }));
  }

  logout() {
      localStorage.removeItem('authUser');
  }
    
  isLoggedIn() {
      return localStorage.getItem('authUser') !== null;
  }

}
