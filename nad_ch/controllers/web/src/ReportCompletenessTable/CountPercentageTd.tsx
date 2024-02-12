import { h } from "preact";

type CountPercentageTdProps = {
  count: number;
  percentage: string;
};

export function CountPercentageTd(props: CountPercentageTdProps) {
  const { count, percentage } = props;
  return (
    <td className="text-right">
      <span className="font-mono-sm">{percentage}</span>
      <br />
      <span className="font-mono-3xs">{count}</span>
    </td>
  );
}
