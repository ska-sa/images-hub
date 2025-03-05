import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { GuestRoutingModule } from './guest-routing.module';

import { SharedModule } from '../shared/shared.module';
import { AngularMaterialModule } from '../angular-material/angular-material.module';
import { ReactiveFormsModule } from '@angular/forms';
import { GuestComponent } from './components/guest/guest.component';
import { RequestDetailsComponent } from './components/request-details/request-details.component';


@NgModule({
  declarations: [
    GuestComponent,
    RequestDetailsComponent
  ],
  imports: [
    CommonModule,
    GuestRoutingModule,
    AngularMaterialModule,
    SharedModule,
    ReactiveFormsModule
  ]
})
export class GuestModule {
  constructor(){
    console.log('Guest Module loaded');
  }
 }
