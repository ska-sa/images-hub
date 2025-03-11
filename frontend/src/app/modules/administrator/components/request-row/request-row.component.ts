import { Component, EventEmitter, Input, Output } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ImageDetailsComponent } from '../../../shared/components/image-details/image-details.component';
import { User } from '../../../../interfaces/user';
import { Image } from '../../../../interfaces/image';
import { UserService } from '../../../../services/user.service';
import { ImageService } from 'src/app/services/image.service';
import { EmailService } from 'src/app/services/email.service';
import { Email } from 'src/app/interfaces/email';

@Component({
  selector: 'app-request-row',
  templateUrl: './request-row.component.html',
  styleUrls: ['./request-row.component.css']
})
export class RequestRowComponent {
  user: User | any = null;
  image: Image | any = null;
  url: string = "";

  @Input() request: Request | any = null;
  @Input() index: number = 0;

  @Output() updateEvent = new EventEmitter<Request>();

  status: string[] = [
    "Pending",
    "Approved",
    "Rejected"
  ];

  constructor(private dialog: MatDialog, private userService: UserService, private imageService: ImageService, private emailService: EmailService) {}

  ngOnInit() :void {
    this.userService.getUser(this.request?.user_id).subscribe({
      next: user => this.user = user,
      error: err => console.log(err) 
    });

    this.imageService.getImage(this.request?.image_id).subscribe({
      next: image => {
        this.image = image;
        // Optionally call getImageUrl here if you want to fetch the image URL immediately
        this.getImageUrl().then(url => {
          this.url = url ?? "";
        });
      },
      error: err => console.log(err) 
    });
  }

  addStatusStyleColor(status: number): any {
    let color = 'orange';
    if (status == 1) {
      color = 'green';
    } else if (status == 2) {
      color = 'red';
    }
    return { color: (true) ? color : '' };
  }

  getEmailAddress(): string | any {
    return this.user?.email_address;
  }

  async getImageUrl(): Promise<string> {
    // Ensure this.image is defined before accessing its properties
    if (this.image && this.image?.high_res_image_filename) {
      const highResResponse = await this.imageService.getImageUrl(this.image?.high_res_image_filename, 'high').toPromise();
      return highResResponse?.url ?? "";
    } else {
      console.error('Image or high_res_image_filename is not defined.');
      return "";
    }
  }

  getImageFilename(): string {
    return this.image.low_res_image_filename;
  }
  
  updateRequest(status: number): void {
    if(this.request) {
      this.request.status = status;
      if(status == 1) {
        const email: Email = {
          receiver_email_address: this.getEmailAddress(),
          subject: "Images Hub Request Approved",
          body: `Hi\n\nWe hope this email finds you well.\n\nWe would like to let you know that your request to access image ${this.image.low_res_image_filename} has been approved.\n\nThanks\n\nKind Regards\nImages Hub Team`
        }
        this.emailService.postEmail(email).subscribe({
          next: ()=> {},
          error: (err)=> console.log(err)
        })

      }

      this.updateEvent.emit(this.request);
    }
  }

  openImageModal(imageUrl: string): void {
    this.dialog.open(ImageDetailsComponent, {
      data: { imageUrl: imageUrl, filename: this.image.low_res_image_filename }
    });
  }
}
