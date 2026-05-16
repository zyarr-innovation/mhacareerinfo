import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

@Component({
  standalone: true,
  imports: [CommonModule, MatButtonModule, MatIconModule],
  templateUrl: './viewer.component.html',
  styleUrls: ['./viewer.component.scss']
})
export class ViewerComponent implements OnInit {
  url?: SafeResourceUrl;
  constructor(private route: ActivatedRoute, private san: DomSanitizer) {}
  ngOnInit() {
    let f = this.route.snapshot.paramMap.get('file');
    const p = this.route.snapshot.paramMap.get('page');
    if (f){
      f = f?.replace('json', 'pdf');
      this.url = this.san.bypassSecurityTrustResourceUrl(`data/${f}#page=${p}`);
    }
  }
}