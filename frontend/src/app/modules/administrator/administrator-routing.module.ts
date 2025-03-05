import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { administratorGuard } from './administrator.guard';
import { AdministratorComponent } from './components/administrator/administrator.component';
import { TableViewComponent } from './components/table-view/table-view.component';
import { GridViewComponent } from '../shared/components/grid-view/grid-view.component';

const routes: Routes = [
  { path: '', component: AdministratorComponent,
    children: [
      { path: '', redirectTo: 'browse-requests', pathMatch: 'full' },
      { path: 'browse-requests', component: TableViewComponent, canActivate: [administratorGuard] },
      { path: 'browse-images', component: GridViewComponent, canActivate: [administratorGuard] }
    ]
  }
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdministratorRoutingModule { }
