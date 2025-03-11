import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-image-details',
  templateUrl: './image-details.component.html',
  styleUrls: ['./image-details.component.css']
})
export class ImageDetailsComponent {
  constructor(
    @Inject(MAT_DIALOG_DATA) public data: { imageUrl: string, filename: string },
    private dialogRef: MatDialogRef<ImageDetailsComponent>
  ) {}

  downloadImage(): void {
    // Directly set the window location to the image URL
    window.location.href = this.data.imageUrl;
  }

  close(): void {
    this.dialogRef.close(); // Close the dialog
  }
}
