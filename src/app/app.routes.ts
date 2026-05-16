import { Routes } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ViewerComponent } from './viewer/viewer.component';

export const routes: Routes = [
  { path: '', component: DashboardComponent },
  { path: 'view/:file/:page', component: ViewerComponent },
  { path: '**', redirectTo: '' }
];