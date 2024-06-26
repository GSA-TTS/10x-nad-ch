import { AlpineComponent } from 'alpinejs';
import { fetchReportData } from '../services';

export type CompletenessReport = {
  features: Feature[];
  overview: Overview;
};

type Overview = {
  data_update_required: boolean;
  etl_update_required: boolean;
  feature_count: number;
  features_flagged: number;
};

type Feature = {
  provided_feature_name: string;
  nad_feature_name: string;
  populated_count: number;
  null_count: number;
  required: boolean;
  status: string;
  populated_percentage: string;
  null_percentage: string;
};

type GroupedFeature = {
  status: string;
  features: Feature[];
};

export interface CompletenessReportComponent {
  id: number;
  isLoading: boolean;
  report: CompletenessReport | null;
  groupedFeatures: GroupedFeature[];
  isGroupedByStatus: boolean;
  buttonText: string;
  toggleButtonClass: string;
  init(): Promise<void>;
  groupFeatures(features: Feature[]): GroupedFeature[];
  getStatusTagClass(status: string): string;
  getNadFieldText(feature: Feature): string;
}

export function CompletenessReport(
  id: string,
): AlpineComponent<CompletenessReportComponent> {
  return {
    id: parseInt(id),
    isLoading: true,
    report: {
      features: [],
      overview: {
        data_update_required: false,
        etl_update_required: false,
        feature_count: 0,
        features_flagged: 0,
      },
    },
    groupedFeatures: [],
    isGroupedByStatus: false,
    async init(): Promise<void> {
      try {
        this.report = await fetchReportData(this.id);
        if (this.report) {
          this.groupedFeatures = this.groupFeatures(this.report.features);
        }
      } catch (error) {
        console.error('Failed to load report:', error);
      } finally {
        this.isLoading = false;
      }
    },
    groupFeatures(features: Feature[]): GroupedFeature[] {
      const groupedByStatus = features.reduce<Record<string, Feature[]>>(
        (acc, obj) => {
          if (!acc[obj.status]) {
            acc[obj.status] = [];
          }
          acc[obj.status].push(obj);
          return acc;
        },
        {},
      );

      return Object.keys(groupedByStatus).map((status) => ({
        status: status,
        features: groupedByStatus[status],
      }));
    },
    get buttonText(): string {
      return this.isGroupedByStatus ? 'Ungroup by Status' : 'Group by Status';
    },
    get toggleButtonClass(): string {
      return this.isGroupedByStatus
        ? 'usa-button-toggle-on'
        : 'usa-button-toggle-off';
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
    getNadFieldText(feature: Feature): string {
      const embellishment = feature.required ? '*' : '';
      return `${embellishment} ${feature.nad_feature_name}`;
    },
  };
}
