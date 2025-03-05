import { Component, Input, OnInit } from '@angular/core';
import { ImageDetailsComponent } from '../image-details/image-details.component';
import { MatDialog } from '@angular/material/dialog';
import { Image } from '../../../../interfaces/image';
import { Request } from '../../../../interfaces/request';
import { environment } from 'src/environments/environment';
import { Link } from '../../../../interfaces/link';
import { LinkService } from '../../../../services/link.service';
import { UserService } from '../../../../services/user.service';
import { RequestService } from '../../../../services/request.service';
import { RequestDetailsComponent } from '../../../../modules/guest/components/request-details/request-details.component';

@Component({
  selector: 'app-image-card',
  templateUrl: './image-card.component.html',
  styleUrls: ['./image-card.component.css']
})
export class ImageCardComponent implements OnInit {
  
  @Input() image: Image | any = null;
  blobUrl: string = ""; // For displaying the image
  filename: string = "";
  isAdministrator: boolean = false;

  constructor(private dialog: MatDialog, private linkService: LinkService, private userService: UserService, public requestService: RequestService) {

  }

  ngOnInit(): void {
    this.createBlobUrl(`${environment.host}/images/${this.image?.low_res_img_fname}`);
    this.filename = this.image.low_res_img_fname.substring(8);
    const user = this.userService.getSignedInUser();
    if(user && user.type == 1){
      this.isAdministrator = true;
    }
  }

  async createBlobUrl(url: string) {
    try {
      const response = await fetch(url);
      const blob = await response.blob();
      this.blobUrl = URL.createObjectURL(blob);
    } catch (error) {
      console.error('Error fetching image:', error);
    }
  }

  generateLink(image_id: number): void {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const timestamp = Date.now().toString(); // Get the current timestamp
    let key = '';

    const limitLength = chars.length - 4;
    // Generate 4 random characters
    for (let i = chars.length - 1; limitLength < i; i--) {
      key += chars.indexOf(chars[i]);
      key += chars[Math.floor(Math.random() * chars.length)];
    }

    // Append the timestamp to the key
    key += timestamp;

    const link: Link = {
      id: 0,
      image_id: image_id,
      key: key,
      limit: 5,
      created_at: ''
    }

    this.linkService.postLink(link).subscribe({
      next: (res) => {
        alert(`Generated Link: ${environment.host}/links/${link.key}`);

      },
      error: err => { console.log(err) }
    });
  }

  async openImageModal(): Promise<void> {
    try {
      const response = await fetch(`${environment.host}/images/${this.image.high_res_img_fname}`);
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);

      this.dialog.open(ImageDetailsComponent, {
        width: 'auto',
        maxWidth: '100vw',  
        data: { imageUrl: url, filename: this.image.low_res_img_fname.substring(8) }
      });
    } catch (error) {
      console.error('Error fetching image:', error);
    }
  }

  async openRequestModel(): Promise<void> {
    try {
      this.dialog.open(RequestDetailsComponent, {
        width: 'auto',
        maxWidth: '100vw',  
        data: { image: this.image }
      });
    } catch (error) {
      console.error('Error fetching request:', error);
    }
  }

  async openModel(): Promise<void> {
    if(this.isAdministrator ) {
      this.openImageModal();
    } else {
      this.requestService.getRequests().subscribe({
        next: (reqs) => { 
          const requests: Request[] = reqs.filter(req => req.user_id == this.userService.getSignedInUser()?.id && req.image_id == this.image?.id  && req?.status == 1 );
          if (requests.length > 0) {
            this.openImageModal();
          } else {
            this.openRequestModel();
          }
        },
        error: err => { console.log(err) }
      });
    }
  }
}
