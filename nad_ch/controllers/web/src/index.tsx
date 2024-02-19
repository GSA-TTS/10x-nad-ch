import "@uswds/uswds/css/uswds.css";
import { h, render } from "preact";
import { ReportCompletenessTable } from "./ReportCompletenessTable";

declare global {
  interface Window {
    completenessReportData: any;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const reportCompletenessTableRoot = document.getElementById(
    "report-completeness-table"
  );

  if (
    reportCompletenessTableRoot &&
    typeof window.completenessReportData !== "undefined"
  ) {
    render(<ReportCompletenessTable />, reportCompletenessTableRoot);
  }
});
