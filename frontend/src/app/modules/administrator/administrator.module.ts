import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AdministratorRoutingModule } from './administrator-routing.module';
import { AngularMaterialModule } from '../angular-material/angular-material.module';
import { SharedModule } from '../shared/shared.module';
import { AdministratorComponent } from './components/administrator/administrator.component';
import { TableViewComponent } from './components/table-view/table-view.component';
import { RequestRowComponent } from './components/request-row/request-row.component';



@NgModule({
  declarations: [
    AdministratorComponent,
    TableViewComponent,
    RequestRowComponent
  ],
  imports: [
    CommonModule,
    AdministratorRoutingModule,
    AngularMaterialModule,
    SharedModule
  ],
  bootstrap: [AdministratorComponent]
})
export class AdministratorModule { 
  constructor(){
    console.log('Adimnistrator Module loaded');
  }
}
