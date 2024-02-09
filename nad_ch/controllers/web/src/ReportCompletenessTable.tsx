import { h, Component, FunctionalComponent } from "preact";

type CountPercentageTdProps = {
  count: number;
  percentage: string;
};

function CountPercentageTd(props: CountPercentageTdProps) {
  const { count, percentage } = props;
  return (
    <td>
      {percentage}
      <br />
      {count}
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

  return (
    <tr>
      <td>{provided_feature_name}</td>
      <td>{nad_feature_name}</td>
      <td>Status</td>
      <CountPercentageTd
        count={populated_count}
        percentage={populated_percentage}
      />
      <CountPercentageTd count={null_count} percentage={null_percentage} />
    </tr>
  );
}

export class ReportCompletenessTable extends Component {
  render() {
    const rows = window.completenessReportData.features.map((obj: any) => (
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
