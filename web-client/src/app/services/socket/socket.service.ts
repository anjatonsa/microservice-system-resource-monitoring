import { Injectable } from '@angular/core';
import { io, Socket } from 'socket.io-client';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SocketService {

  private socket!: Socket;
  private messages: Array<any> =[];
  constructor() {
    this.connectToSocket();
  }

  private connectToSocket(): void {
    this.socket = io('http://localhost:5003'); 

    this.socket.on('connect', () => {
      console.log('Connected to WebSocket server');
    });

    this.socket.on('data-notf', (data) => {
      console.log('Received data from server:', data);
      this.messages.push(data);
      if (this.messages.length > 20) {
        this.messages = this.messages.slice(-20); 
      }

    });

    this.socket.on('disconnect', () => {
      console.log('Disconnected from WebSocket server');
    });
  }

  public sendMessage(msg: string): void {
    this.socket.emit('new-message-s', { message: msg });
  }


  public getMessages(): Observable<any> {
    return new Observable((observer) => {
      this.socket.on('data-notf', (data) => {
        observer.next(data);
        console.log("proslo ovde")
      });
    });
  }

}
