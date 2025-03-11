import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Image } from '../interfaces/image';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

interface S3Image {
  id: number;
  url: string;
}

@Injectable({
  providedIn: 'root'
})
export class ImageService {

  baseUrl: string = `${environment.host}/images`;

  constructor(private http: HttpClient) { }

  private getAuthHeader(): HttpHeaders {
    return new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${ environment.apiKey}`
    });
  }

  getImages(): Observable<Image[]> {
    return this.http.get<Image[]>(this.baseUrl, {
      headers: this.getAuthHeader()
    });
  }

  getImage(id: number): Observable<Image> {
    return this.http.get<Image>(`${this.baseUrl}/${id}`, {
      headers: this.getAuthHeader()
    });
  }

  getImageUrl(filename: string, resolution: 'low' | 'high'): Observable<S3Image> {
    const url = `${environment.host}/images/${filename}?resolution=${resolution}`;
    return this.http.get<S3Image>(url, {
      headers: this.getAuthHeader()
    });
  }

  uploadImages(formData: FormData): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}`, formData, { // Ensure the correct endpoint
      headers: new HttpHeaders({
        'Authorization': `Bearer ${ environment.apiKey}`
      }), // You may not need to set Content-Type here
      reportProgress: true,
      observe: 'events'
    });
  }  
}
