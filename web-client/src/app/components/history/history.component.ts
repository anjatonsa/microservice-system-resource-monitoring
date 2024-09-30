import { Component } from '@angular/core';
import { ApigatewayService } from '../../services/apigateway/apigateway.service';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-history',
  standalone: true,
  imports: [],
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.css'] // Corrected property name from `styleUrl` to `styleUrls`
})
export class HistoryComponent {
  snapshot_url!: SafeResourceUrl; // Use definite assignment assertion to avoid initialization error

  constructor(private apiGatewayService: ApigatewayService, private sanitizer: DomSanitizer) {}

  ngOnInit(): void {
    this.apiGatewayService.getHistory().subscribe((message: any) => {
      // Sanitize the URL before assigning it
      this.snapshot_url = this.sanitizer.bypassSecurityTrustResourceUrl(message.snapshot_url);
      console.log('snap message:', this.snapshot_url);
    });
  }
}
