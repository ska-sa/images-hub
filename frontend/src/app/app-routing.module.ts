import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SignInComponent } from './components/sign-in/sign-in.component';

const routes: Routes = [
  { path: 'guest', loadChildren: () => import('./modules/guest/guest.module').then(m => m.GuestModule) }, 
  { path: 'administrator', loadChildren: () => import('./modules/administrator/administrator.module').then(m => m.AdministratorModule) },
  { path: 'sign-in', component: SignInComponent },
  { path: '', redirectTo: '/sign-in', pathMatch: 'full' },
  { path: '**', redirectTo: '/sign-in', pathMatch: 'full' } // Catch all unknown routes and redirect to sign-in
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { bindToComponentInputs: true })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
