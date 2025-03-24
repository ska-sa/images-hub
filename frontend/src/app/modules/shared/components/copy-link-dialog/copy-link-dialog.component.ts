import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-copy-link-dialog',
  templateUrl: './copy-link-dialog.component.html',
  styleUrls: ['./copy-link-dialog.component.css']
})
export class CopyLinkDialogComponent implements OnInit {
  copied: boolean = false; // Track if the link has been copied

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: { title: string, link: string },
    private dialogRef: MatDialogRef<CopyLinkDialogComponent>
  ) {}

  ngOnInit(): void {
    // Automatically copy the link to the clipboard
    this.copyToClipboard(this.data.link);
    
    // Set copied state to true and automatically close the dialog after 5 seconds
    this.copied = true;
    setTimeout(() => {
      this.close();
    }, 5000);
  }

  copyToClipboard(link: string): void {
    const textarea = document.createElement('textarea');
    textarea.value = link;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
  }

  close(): void {
    this.dialogRef.close(); // Close the dialog
  }
}
