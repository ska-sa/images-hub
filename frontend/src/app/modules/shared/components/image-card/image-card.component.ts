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
import { ImageService } from '../../../../services/image.service';
import { MessageDialogComponent } from '../message-dialog/message-dialog.component';
import { CopyLinkDialogComponent } from '../copy-link-dialog/copy-link-dialog.component';

interface S3Image {
  id: number;
  url: string;
}

@Component({
  selector: 'app-image-card',
  templateUrl: './image-card.component.html',
  styleUrls: ['./image-card.component.css']
})
export class ImageCardComponent implements OnInit {
  
  @Input() image: Image | any = null;
  blobUrl: string = ""; // For displaying the image
  filename: string = "";
  url: string = "";
  highResUrl: string = "";
  isAdministrator: boolean = false;

  lowResResponse: any = null;
  highResResponse: any = null;

  constructor(private dialog: MatDialog, private linkService: LinkService, private userService: UserService, public requestService: RequestService, public imageService: ImageService) {

  }

  async ngOnInit(): Promise<void> {

    const user = this.userService.getSignedInUser();
    if(user && user.type == 1){
      this.isAdministrator = true;
    }
    //console.log(`User type ${this.isAdministrator} ${user?.type}`)

    this.lowResResponse = await this.imageService.getImageUrl(this.image.low_res_image_filename, 'low').toPromise();
    this.highResResponse = await this.imageService.getImageUrl(this.image.high_res_image_filename, 'high').toPromise();
    //this.createBlobUrl(lowResResponse?.url ?? "");
  
    this.filename = this.image.high_res_image_filename;
    this.url = this.highResResponse?.url ?? '';
    this.highResUrl = this.url;
    if (! this.isAdministrator) {
      this.filename = this.image.low_res_image_filename;
      this.url = this.lowResResponse?.url ?? '';
    }

    //console.log(this.filename);
    //console.log(lowResResponse?.url);
    
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
        //alert(`Generated Link: ${environment.host}/links/${link.key}`);
        const generatedLink = `${environment.host}/links/${link.key}`; // Generated link to download this image
        this.openCopyLinkDialog('Link Generated!', generatedLink);
      },
      error: err => { console.log(err) }
    });
  }

  openCopyLinkDialog(title: string, link: string): void {
    this.dialog.open(CopyLinkDialogComponent, {
      data: {
        title: title,
        link: link
      },
      width: 'auto',
      maxWidth: '100vw'
    });
  }

  async openImageModal(): Promise<void> {
    try {
      this.dialog.open(ImageDetailsComponent, {
        width: 'auto',
        maxWidth: '100vw',  
        data: { imageUrl: this.url, filename: this.image.low_res_image_filename }
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

  async openMessageModel(title: string, message: string): Promise<void> {
    try{
      this.dialog.open(MessageDialogComponent, {
        width: 'auto',
        maxWidth: '100vw',
        data: {
          title: title,
          message: message
        }
      });
    } catch (error) {
      console.log(`Error ${error}`)
    }
  }

  async openModel(): Promise<void> {
    if(this.isAdministrator) {
      this.openImageModal();
    } else {
      this.requestService.getRequests().subscribe({
        next: (reqs) => { 
          const requests: Request[] = reqs.filter(req => req.user_id == this.userService.getSignedInUser()?.id && req.image_id == this.image?.id);
          let status = 3
          if(requests.length > 0) {
            status = requests[0].status;
          }
          switch(status){
            case 0:
              this.openMessageModel("Request Already Sent!", `Hi,<br /><br />You have already sent a request for this image ${this.image.low_res_image_filename}.<br /><br />Please wait for the administrators to approve your request.<br /><br />Thanks<br /><br />Kind Regards<br />Images Hub Team`);
              break;
            case 1:
              this.url = this.highResResponse?.url ?? '';
              this.openImageModal();
              break;
            case 2:
              this.openMessageModel("Request Rejected!", "Hi<br /><br />We regret to let you know that out administrators have decided to reject your request.<br /><br />Kind Regards<br />Images Hub Team");
              break;
            default:
              this.openRequestModel();
          }
         /* 
          if (requests.length > 0) {
            this.url = this.highResUrl;
            this.openImageModal();
          } else {
            const r: Request[] = reqs.filter(req => req.user_id == this.userService.getSignedInUser()?.id && req.image_id == this.image?.id  && req?.status == 0 );
            if(r.length > 0) {
              this.openMessageModel();
            } else {
              this.openRequestModel();
            }
          }*/
        },
        error: err => { console.log(err) }
      });
    }
  }
}
