import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { NotificationComponent } from './components/notification/notification.component';
import { authGuard } from './services/auth/auth.guard';
import { PageComponent } from './components/page/page.component';
import { SignupComponent } from './components/signup/signup.component';

export const routes: Routes = [  { path: 'login', component: LoginComponent },
    { path: 'notifications', component: NotificationComponent,canActivate: [authGuard] },
    { path: 'page', component: PageComponent,canActivate: [authGuard] },
    { path: 'signup', component: SignupComponent},
    { path: '', redirectTo: '/login', pathMatch: 'full' },];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }