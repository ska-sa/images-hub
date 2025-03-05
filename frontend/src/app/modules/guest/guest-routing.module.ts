import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { guestGuard } from './guest.guard';
import { GuestComponent } from './components/guest/guest.component';
import { GridViewComponent } from '../shared/components/grid-view/grid-view.component';

const routes: Routes = [
  { path: '', component: GuestComponent,
    children: [
      { path: '', redirectTo: 'browse-images', pathMatch: 'full' },
      { path: 'browse-images', component: GridViewComponent, canActivate: [guestGuard] }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class GuestRoutingModule { }
