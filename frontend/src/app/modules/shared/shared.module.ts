import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from './components/header/header.component';
import { FormsModule } from '@angular/forms';
import { GridViewComponent } from './components/grid-view/grid-view.component';
import { RouterModule } from '@angular/router';
import { ImageDetailsComponent } from './components/image-details/image-details.component';
import { MatDialogModule } from '@angular/material/dialog';
import { ImageCardComponent } from './components/image-card/image-card.component';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MessageDialogComponent } from './components/message-dialog/message-dialog.component';
import { CopyLinkDialogComponent } from './components/copy-link-dialog/copy-link-dialog.component';

const matertialComponent = [
  MatIconModule,
  MatProgressSpinnerModule
];

@NgModule({
  declarations: [
    HeaderComponent,
    GridViewComponent,
    ImageDetailsComponent,
    ImageCardComponent,
    MessageDialogComponent,
    CopyLinkDialogComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    MatDialogModule,
    matertialComponent
  ],
  exports: [
    HeaderComponent,
    ImageDetailsComponent,
    MatDialogModule,
    ImageCardComponent,
    matertialComponent
  ]
})
export class SharedModule { }
