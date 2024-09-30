import { Component, inject } from '@angular/core';
import { Router } from '@angular/router'
import { AuthService } from '../../services/auth/auth.service';
import { NotificationComponent } from '../notification/notification.component';
import { HistoryComponent } from '../history/history.component';

@Component({
  selector: 'app-page',
  standalone: true,
  imports: [NotificationComponent, HistoryComponent],
  templateUrl: './page.component.html',
  styleUrl: './page.component.css'
})
export class PageComponent {

  authService = inject(AuthService);
  router = inject(Router);
  public logout(){
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
