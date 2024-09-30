import { Component } from '@angular/core';
import { AuthService } from '../../services/auth/auth.service';
import { inject } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ ReactiveFormsModule, RouterModule ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  username: string = '';
  password: string = '';
  errorMessage: string = '';
  hidePassword: boolean = true;

  authService = inject(AuthService);
  router = inject(Router);

  protected loginForm = new FormGroup({
    username: new FormControl('', [Validators.required]),
    password: new FormControl('', [Validators.required])
  })

  onSubmit(){
    if(this.loginForm.valid){
      console.log(this.loginForm.value);
      if(this.loginForm.value.username && this.loginForm.value.password)
        this.authService.login(this.loginForm.value.username,this.loginForm.value.password)
        .subscribe((data: any) => {
          if(this.authService.isLoggedIn()){
            this.router.navigate(['/page']);
          }
        });
    }
  }

}
