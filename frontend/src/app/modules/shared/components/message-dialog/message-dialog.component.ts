import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';


@Component({
  selector: 'app-message-dialog',
  templateUrl: './message-dialog.component.html',
  styleUrls: ['./message-dialog.component.css']
})
export class MessageDialogComponent implements OnInit {
  constructor(
    @Inject(MAT_DIALOG_DATA) public data: { title: string, message: string },
    private dialogRef: MatDialogRef<MessageDialogComponent>
  ) {}

  ngOnInit(): void {
    // Automatically close the dialog after 5 seconds
    setTimeout(() => {
      this.close();
    }, 5000);
  }

  close(): void {
    this.dialogRef.close(); // Close the dialog
  }
}
