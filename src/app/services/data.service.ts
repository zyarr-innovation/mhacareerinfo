import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CollegeRecord } from '../models/dashboard.model';

@Injectable({ providedIn: 'root' })
export class DataService {
  constructor(private http: HttpClient) {}

  getFileRegistry(): Observable<string[]> {
    return this.http.get<string[]>('assets/file-registry.json');
  }

  getRecordsByFile(fileName: string): Observable<CollegeRecord[]> {
    return this.http.get<CollegeRecord[]>(`assets/${fileName}`);
  }
}