export interface CollegeRecord {
  name: string;
  status: string;
  cap_seats: number;
  course_name: string;
  page_no: string;
}

export interface FlattenedRow {
  isHeader: boolean;
  collegeName: string;
  courseName?: string;
  seats?: number;
  pageNo?: string;
  fileName?: string;
}