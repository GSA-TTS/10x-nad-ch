import { h } from "preact";
import { CountPercentageTd } from "./CountPercentageTd";
import { StatusTd } from "./StatusTd";

export type RowProps = {
  required: boolean;
  status: string;
  provided_feature_name: string;
  nad_feature_name: string;
  populated_count: number;
  populated_percentage: string;
  null_count: number;
  null_percentage: string;
};

export function Row(props: RowProps) {
  const {
    required,
    status,
    provided_feature_name,
    nad_feature_name,
    populated_count,
    populated_percentage,
    null_count,
    null_percentage,
  } = props;

  return (
    <tr>
      <td>{provided_feature_name}</td>
      <td>
        {required && <span>* </span>}
        {nad_feature_name}
      </td>
      <StatusTd status={status} />
      <CountPercentageTd count={null_count} percentage={null_percentage} />
      <CountPercentageTd
        count={populated_count}
        percentage={populated_percentage}
      />
    </tr>
  );
}
