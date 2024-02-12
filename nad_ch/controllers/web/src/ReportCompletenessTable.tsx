import { h, Component } from "preact";

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

function StatusTd({ status }: StatusTdProps) {
  const statusClass = `usa-tag ${
    statusClassMapping[status] || "usa-tag__info"
  }`;

  return (
    <td>
      <span className={statusClass}>{status}</span>
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
  required: boolean;
  status: string;
  provided_feature_name: string;
  nad_feature_name: string;
  populated_count: number;
  populated_percentage: string;
  null_count: number;
  null_percentage: string;
};

function Row(props: RowProps) {
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

type ReportCompletenessTableState = {
  featureData: [];
  isGrouped: boolean;
};

export class ReportCompletenessTable extends Component<
  {},
  ReportCompletenessTableState
> {
  constructor() {
    super();
    this.state = {
      featureData: [],
      isGrouped: false,
    };

    this.toggleGrouped = this.toggleGrouped.bind(this);
  }

  componentDidMount() {
    const sortedFeatureData = window.completenessReportData.features.sort(
      (a: RowProps, b: RowProps) => b.populated_count - a.populated_count
    );

    this.setState(() => ({
      featureData: sortedFeatureData,
    }));
  }

  toggleGrouped = () => {
    this.setState((prevState) => {
      const isGrouped = !prevState.isGrouped;
      const featureData = prevState.featureData.sort(
        (a: RowProps, b: RowProps) => {
          if (isGrouped) {
            const statusOrder: any = {
              Rejected: 1,
              "Updated by calculation": 2,
              "Custom ETL needed": 3,
              "No error": 4,
            };
            return (
              (statusOrder[a.status] || Number.MAX_VALUE) -
              (statusOrder[b.status] || Number.MAX_VALUE)
            );
          } else {
            return b.populated_count - a.populated_count;
          }
        }
      );

      return { isGrouped, featureData };
    });
  };

  render() {
    const rows = this.state.featureData.map((obj: any) => (
      <Row key={obj.provided_feature_name} {...(obj as RowProps)} />
    ));

    const buttonClass = `usa-button ${
      this.state.isGrouped ? "usa-button-toggle-on" : "usa-button-toggle-off"
    }`;
    const buttonText = this.state.isGrouped
      ? "Grouped By Status"
      : "Group By Status";

    return (
      <div class="padding-top-2">
        <ul class="usa-button-group usa-button-group-toggle">
          <li class="usa-button-group__item">
            <button
              type="button"
              class={buttonClass}
              onClick={this.toggleGrouped}
            >
              {buttonText}
            </button>
          </li>
          <li>
            <button type="button" class="usa-button">
              Download .gdb
            </button>
          </li>
        </ul>
        <div class="usa-table-default">
          <table class="usa-table usa-table--borderless width-full">
            <thead class="width-full">
              <tr>
                <th scope="col">Submitted Field</th>
                <th scope="col">
                  <div class="usa-tooltip" data-position="top" title="Required">
                    *
                  </div>{" "}
                  NAD Field
                </th>
                <th scope="col">Status</th>
                <th scope="col">Empty</th>
                <th scope="col">Populated</th>
              </tr>
            </thead>
            <tbody>{rows}</tbody>
          </table>
        </div>
      </div>
    );
  }
}
