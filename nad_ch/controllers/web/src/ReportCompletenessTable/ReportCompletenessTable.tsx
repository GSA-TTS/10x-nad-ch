import { h, Component } from "preact";
import { RowProps, Row } from "./Row";

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
    const rows = this.state.featureData.map((obj: any) => {
      const { isGrouped: _, ...otherProps } = obj as RowProps;
      const isGrouped = this.state.isGrouped;

      return (
        <Row
          key={obj.provided_feature_name}
          isGrouped={isGrouped}
          {...otherProps}
        />
      );
    });

    const buttonClass = `usa-button ${
      this.state.isGrouped ? "usa-button-toggle-on" : "usa-button-toggle-off"
    }`;

    const thClass = this.state.isGrouped ? "grouped" : "";

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
        <div class="usa-table-report">
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
                <th scope="col" className={thClass}>
                  Status
                </th>
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
