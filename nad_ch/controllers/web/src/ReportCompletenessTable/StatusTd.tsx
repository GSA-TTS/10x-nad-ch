import { h } from "preact";

type StatusTdProps = {
  status:
    | "No error"
    | "Updated by calculation"
    | "Rejected"
    | "Custom ETL required"
    | string;
};

const statusClassMapping: { [key in StatusTdProps["status"]]?: string } = {
  "No error": "usa-tag__success",
  "Updated by calculation": "usa-tag__warning",
  Rejected: "usa-tag__error",
};

export function StatusTd({ status }: StatusTdProps) {
  const statusClass = `usa-tag ${
    statusClassMapping[status] || "usa-tag__info"
  }`;

  return (
    <td>
      <span className={statusClass}>{status}</span>
    </td>
  );
}
