/**
 * @jest-environment jsdom
 */

import {
  CompletenessReport,
  CompletenessReportComponent,
} from './CompletenessReport';
import { AlpineComponent } from 'alpinejs';
import { fetchReportData } from '../services';

jest.mock('../services', () => ({
  fetchReportData: jest.fn(),
}));

describe('CompletenessReportComponent', () => {
  let component: AlpineComponent<CompletenessReportComponent>;
  const mockReportData = {
    features: [
      {
        provided_feature_name: 'AddNum_Pre',
        nad_feature_name: 'AddNum_Pre',
        populated_count: 1141,
        null_count: 0,
        required: false,
        status: 'No error',
        populated_percentage: '100%',
        null_percentage: '0%',
      },
      {
        provided_feature_name: 'Add_Number',
        nad_feature_name: 'Add_Number',
        populated_count: 1141,
        null_count: 0,
        required: true,
        status: 'No error',
        populated_percentage: '100%',
        null_percentage: '0%',
      },
    ],
    overview: {
      data_update_required: false,
      etl_update_required: false,
      feature_count: 10,
      features_flagged: 2,
    },
  };

  beforeEach(() => {
    (fetchReportData as jest.Mock).mockResolvedValue(mockReportData);
    component = CompletenessReport('1');
  });

  it('initializes with default data', () => {
    expect(component.id).toBe(1);
    expect(component.isLoading).toBe(true);
    expect(component.groupedFeatures).toEqual([]);
    expect(component.isGroupedByStatus).toBe(false);
  });

  it('loads report data on init', async () => {
    await component.init();
    expect(fetchReportData).toHaveBeenCalledWith(1);
    expect(component.isLoading).toBe(false);
    expect(component.report).toEqual(mockReportData);
  });

  it('groups features by status', () => {
    component.report = mockReportData;
    const groupedFeatures = component.groupFeatures(mockReportData.features);
    expect(groupedFeatures).toEqual([
      {
        status: 'No error',
        features: [
          {
            provided_feature_name: 'AddNum_Pre',
            nad_feature_name: 'AddNum_Pre',
            populated_count: 1141,
            null_count: 0,
            required: false,
            status: 'No error',
            populated_percentage: '100%',
            null_percentage: '0%',
          },
          {
            provided_feature_name: 'Add_Number',
            nad_feature_name: 'Add_Number',
            populated_count: 1141,
            null_count: 0,
            required: true,
            status: 'No error',
            populated_percentage: '100%',
            null_percentage: '0%',
          },
        ],
      },
    ]);
  });

  it('computes buttonText based on isGroupedByStatus', () => {
    expect(component.buttonText).toBe('Group by Status');
    component.isGroupedByStatus = true;
    expect(component.buttonText).toBe('Ungroup by Status');
  });

  it('computes toggleButtonClass based on isGroupedByStatus', () => {
    expect(component.toggleButtonClass).toBe('usa-button-toggle-off');
    component.isGroupedByStatus = true;
    expect(component.toggleButtonClass).toBe('usa-button-toggle-on');
  });

  it('gets status tag class based on different statuses', () => {
    expect(component.getStatusTagClass('No error')).toBe('usa-tag__success');
    expect(component.getStatusTagClass('Updated by calculation')).toBe(
      'usa-tag__warning',
    );
    expect(component.getStatusTagClass('Rejected')).toBe('usa-tag__error');
    expect(component.getStatusTagClass('Other')).toBe('usa-tag__info');
  });
});
