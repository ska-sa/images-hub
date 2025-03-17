import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AdministratorRoutingModule } from './administrator-routing.module';
import { AngularMaterialModule } from '../angular-material/angular-material.module';
import { SharedModule } from '../shared/shared.module';
import { AdministratorComponent } from './components/administrator/administrator.component';
import { TableComponent } from './components/table/table.component';
import { RowComponent } from './components/row/row.component';



@NgModule({
  declarations: [
    AdministratorComponent,
    TableComponent,
    RowComponent
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
