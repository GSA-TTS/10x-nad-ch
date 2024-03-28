import { AlpineComponent } from 'alpinejs';
import { BASE_URL } from '../config';

export interface CompletenessReportComponent {
  id: number;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  report: any;
  isGroupedByStatus: boolean;
  buttonText: string;
  getStatusTagClass(status: string): string;
}

export function CompletenessReport(
  id: string,
): AlpineComponent<CompletenessReportComponent> {
  return {
    id: parseInt(id),
    report: [],
    isGroupedByStatus: false,
    async init(): Promise<void> {
      const response = await fetch(`${BASE_URL}/api/reports/${this.id}`);
      const reportData = await response.json();
      this.report = JSON.parse(reportData);
      console.log(this.report);
    },
    get buttonText(): string {
      return this.isGroupedByStatus ? 'Ungroup by Status' : 'Group by Status';
    },
    getStatusTagClass(status: string): string {
      switch (status) {
        case 'No error':
          return 'usa-tag__success';
        case 'Updated by calculation':
          return 'usa-tag__warning';
        case 'Rejected':
          return 'usa-tag__error';
        default:
          return 'usa-tag__info';
      }
    },
  };
}
