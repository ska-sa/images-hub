import { Component, EventEmitter, Output } from '@angular/core';
import { Image } from '../../../../interfaces/image';
import { ImageService } from '../../../../services/image.service';
import { UserService } from '../../../../services/user.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-grid-view',
  templateUrl: './grid-view.component.html',
  styleUrls: ['./grid-view.component.css']
})
export class GridViewComponent {
  imagesList: Image[] = [];
  filteredImagesList: Image[] = [];
  isAdministrator: boolean = false;

  isLoading: boolean = true;

  isDragActive: boolean = false;
  files: File[] = [];
  constructor(
    private imageService: ImageService,
    private userService: UserService,
    private http: HttpClient
  ) {}

  ngOnInit(): void {
    this.loadData();
    this.userService.filterSubject.subscribe(filter => {
      this.search(filter);
    });

    const user = this.userService.getSignedInUser();
    if(user && user.type == 1){
      this.isAdministrator = true;
    } else {
      this.isAdministrator = false;
    }
  }

  search(filename: string): void {
    this.filteredImagesList = [];
    if (filename != "") {
      this.imagesList.forEach(image => {
        if (image.low_res_image_filename.toLowerCase().includes(filename.toLowerCase()))
          this.filteredImagesList.push(image);
      });
    } else {
      this.filteredImagesList = this.imagesList;
    }
  }

  loadData(): void {
    this.isLoading = true;
    this.imageService.getImages().subscribe({
      next: (imgsList) => {
        this.imagesList = imgsList;
        this.filteredImagesList = imgsList;
        this.isLoading = false;
      },
      error: err => {
        console.log(err);
        this.isLoading = false;
      }
    });
  }

  onDragOver(event: DragEvent): void {
    event.preventDefault();
    this.isDragActive = true;
  }

  onDragEnter(event: DragEvent): void {
    event.preventDefault();
    this.isDragActive = true;
  }

  onDragLeave(event: DragEvent): void {
    event.preventDefault();
    this.isDragActive = false;
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    this.isDragActive = false;
    this.files = event.dataTransfer?.files ? Array.from(event.dataTransfer.files) : [];
    this.uploadFilesToS3(this.files);
  }

  uploadFilesToS3(files: File[]): void {
    if (files.length) {
      const formData = new FormData();
      files.forEach(file => formData.append('file', file)); // Ensure the key is 'file'
  
      this.imageService.uploadImages(formData).subscribe({
        next: (response) => {
          //console.log('Upload Success:', response);
          this.loadData(); // Optionally reload data or handle the response
        },
        error: (error) => {
          console.error('Upload Error:', error);
        }
      });
    }
  }
  
  onFileSelected(event: any): void {
    const files = Array.from(event.target.files) as File[];
    this.uploadFilesToS3(files);
  }
}
