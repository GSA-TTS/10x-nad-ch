import { BASE_URL } from './config';
import { CompletenessReport } from './components/CompletenessReport';

export async function fetchReportData(id: number): Promise<CompletenessReport> {
  const response = await fetch(`${BASE_URL}/api/reports/${id}`);
  const reportData = await response.json();
  return reportData;
}
