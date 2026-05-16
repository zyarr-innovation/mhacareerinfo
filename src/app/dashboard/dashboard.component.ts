import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { DataService } from '../services/data.service';
import { CollegeRecord, FlattenedRow } from '../models/dashboard.model';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  fileTabs: { name: string; label: string }[] = [];
  activeFileName = '';
  
  currentRecords: CollegeRecord[] = [];
  displayRows: FlattenedRow[] = [];
  
  collegeSearch = '';
  courseSearch = '';

  constructor(private dataService: DataService, private router: Router) {}

  ngOnInit() {
    this.dataService.getFileRegistry().subscribe(files => {
      if (files && files.length > 0) {
        this.fileTabs = files.map(file => ({
          name: file,
          label: file.replace(/[-_]/g, ' ').replace('.json', '')
        }));
        this.selectTab(files[0]);
      }
    });
  }

  selectTab(fileName: string) {
    this.activeFileName = fileName;
    this.dataService.getRecordsByFile(fileName).subscribe(records => {
      this.currentRecords = records;
      this.applyFilters();
    });
  }

  applyFilters() {
    const colQ = this.collegeSearch.toLowerCase().trim();
    const couQ = this.courseSearch.toLowerCase().trim();
    const tempRows: FlattenedRow[] = [];

    const collegeMap = new Map<string, CollegeRecord[]>();
    this.currentRecords.forEach(r => {
      if (!collegeMap.has(r.name)) collegeMap.set(r.name, []);
      collegeMap.get(r.name)!.push(r);
    });

    Array.from(collegeMap.keys()).sort().forEach(name => {
      const records = collegeMap.get(name)!;
      const filteredCourses = couQ 
        ? records.filter(c => c.course_name.toLowerCase().includes(couQ))
        : records;
      
      if (filteredCourses.length > 0 && name.toLowerCase().includes(colQ)) {
        tempRows.push({ isHeader: true, collegeName: name });
        filteredCourses.forEach(c => tempRows.push({
          isHeader: false,
          collegeName: name,
          courseName: c.course_name, 
          seats: c.cap_seats, 
          pageNo: c.page_no
        }));
      }
    });
    this.displayRows = tempRows;
  }

  openPdf(pageNo?: string) {
    if (this.activeFileName && pageNo) {
      this.router.navigate(['/view', this.activeFileName, pageNo]);
    }
  }
}