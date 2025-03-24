import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-copy-link-dialog',
  templateUrl: './copy-link-dialog.component.html',
  styleUrls: ['./copy-link-dialog.component.css']
})
export class CopyLinkDialogComponent implements OnInit {
  copied: boolean = false;
  copyLinkButtonText: string = 'Copy';

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: { title: string, link: string },
    private dialogRef: MatDialogRef<CopyLinkDialogComponent>
  ) {}

  ngOnInit(): void {
    // Do nothing, wait for user to click the button
  }

  copyToClipboard(link: string): void {
    navigator.clipboard.writeText(link)
      .then(() => {
        this.copied = true;
        this.copyLinkButtonText = 'Copied';
        setTimeout(() => {
          this.close();
        }, 2000);
      })
      .catch((error) => {
        console.error('Failed to copy text: ', error);
      });
  }

  toggleCopyState(): void {
    if (!this.copied) {
      this.copyToClipboard(this.data.link);
    } else {
      this.close();
    }
  }

  close(): void {
    this.dialogRef.close(); // Close the dialog
  }
}
