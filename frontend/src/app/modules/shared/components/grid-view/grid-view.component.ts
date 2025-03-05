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
  }

  search(filename: string): void {
    this.filteredImagesList = [];
    if (filename != "") {
      this.imagesList.forEach(image => {
        if (image.low_res_img_fname.substring(8).toLowerCase().includes(filename.toLowerCase()))
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
    this.uploadFilesToDropbox(this.files);
  }

  uploadFilesToDropbox(files: File[]): void {
    
  }

  onFileSelected(event: any): void {
    const files = Array.from(event.target.files) as File[];
    this.uploadFilesToDropbox(files);
  }
}
