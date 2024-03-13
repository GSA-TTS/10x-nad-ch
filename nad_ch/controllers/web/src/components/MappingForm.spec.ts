/**
 * @jest-environment jsdom
 */

import MappingForm from './MappingForm';
import { BASE_URL } from '../config';
import { navigateTo } from '../utilities';

jest.mock('../utilities', () => ({
  navigateTo: jest.fn(),
}));

describe('MappingForm', () => {
  let mappingForm: any;

  beforeEach(() => {
    mappingForm = MappingForm();
  });

  it('should initialize with correct initial state', () => {
    expect(mappingForm.hasError).toBe(false);
    expect(mappingForm.errorMessage).toBe('');
    expect(mappingForm.title).toBe('');
  });

  it('should set error state and message when title is invalid', () => {
    mappingForm.title = 'Invalid Title';

    mappingForm.createMapping();

    expect(mappingForm.hasError).toBe(true);
    expect(mappingForm.errorMessage).toBe(
      'Name can only contain letters and numbers',
    );
  });

  it('should navigate to create mapping page when title is valid', () => {
    const validTitle = 'ValidTitle123';
    mappingForm.title = validTitle;

    mappingForm.createMapping();

    expect(mappingForm.hasError).toBe(false);
    expect(navigateTo).toHaveBeenCalledWith(
      `${BASE_URL}/mappings/create?title=${encodeURIComponent(validTitle)}`,
    );
  });

  it('should reset state and close modal', () => {
    mappingForm.hasError = true;
    mappingForm.errorMessage = 'Error message';
    mappingForm.title = 'Some title';

    mappingForm.closeModal();

    expect(mappingForm.hasError).toBe(false);
    expect(mappingForm.errorMessage).toBe('');
    expect(mappingForm.title).toBe('');
  });
});
