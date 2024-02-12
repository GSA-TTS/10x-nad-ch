import { h, Component } from "preact";

type StatusTdProps = {
  status: string;
};

function StatusTd(props: StatusTdProps) {
  const { status } = props;
  let statusClass = "usa-tag__info";
  if (status === "No error") {
    statusClass = "usa-tag__success";
  } else if (status === "Updated by calculation") {
    statusClass = "usa-tag__warning";
  } else if (status === "Rejected") {
    statusClass = "usa-tag__error";
  }

  return (
    <td>
      <span className={`usa-tag ${statusClass}`}>{status}</span>
    </td>
  );
}

type CountPercentageTdProps = {
  count: number;
  percentage: string;
};

function CountPercentageTd(props: CountPercentageTdProps) {
  const { count, percentage } = props;
  return (
    <td className="text-right">
      <span className="font-mono-sm">{percentage}</span>
      <br />
      <span className="font-mono-3xs">{count}</span>
    </td>
  );
}

type RowProps = {
  provided_feature_name: string;
  nad_feature_name: string;
  populated_count: number;
  populated_percentage: string;
  null_count: number;
  null_percentage: string;
};

function Row(props: RowProps) {
  const {
    provided_feature_name,
    nad_feature_name,
    populated_count,
    populated_percentage,
    null_count,
    null_percentage,
  } = props;

  function getRandomStatus(): string {
    const statuses = [
      "No error",
      "Rejected",
      "Updated by calculation",
      "Custom ETL needed",
    ];
    const randomIndex = Math.floor(Math.random() * statuses.length);
    return statuses[randomIndex];
  }

  return (
    <tr>
      <td>{provided_feature_name}</td>
      <td>{nad_feature_name}</td>
      <StatusTd status={getRandomStatus()} />
      <CountPercentageTd count={null_count} percentage={null_percentage} />
      <CountPercentageTd
        count={populated_count}
        percentage={populated_percentage}
      />
    </tr>
  );
}

export class ReportCompletenessTable extends Component {
  render() {
    const rows = window.completenessReportData.features
      .sort((a: RowProps, b: RowProps) => b.populated_count - a.populated_count)
      .map((obj: any) => (
        <Row key={obj.provided_feature_name} {...(obj as RowProps)} />
      ));

    return (
      <div class="usa-table-default">
        <table class="usa-table usa-table--borderless width-full">
          <thead class="width-full">
            <tr>
              <th scope="col">Submitted Field</th>
              <th scope="col">NAD Field</th>
              <th scope="col">Status</th>
              <th scope="col">Empty</th>
              <th scope="col">Populated</th>
            </tr>
          </thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    );
  }
}
