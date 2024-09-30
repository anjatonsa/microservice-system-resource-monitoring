import { HttpClient, HttpHeaders } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApigatewayService {

  constructor() { }
  httpClient = inject(HttpClient);
  baseUrl = 'http://localhost:5003';

  getHistory() {
    const authUserString = localStorage.getItem("authUser");
    if (authUserString) {
      const authUser = JSON.parse(authUserString);
      const tok = authUser.token;
  
      console.log(tok);
      const token = 'Bearer ' + tok;

      const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': token
      });
      return this.httpClient.get(`${this.baseUrl}/snapshot`, {headers});
  }
  return of({ error: 'Authentication token not found' });
}
}
