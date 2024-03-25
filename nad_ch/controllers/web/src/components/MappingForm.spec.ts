/**
 * @jest-environment jsdom
 */

import { MappingForm, MappingFormComponent } from './MappingForm';
import { BASE_URL } from '../config';
import { navigateTo } from '../utilities';
import { AlpineComponent } from 'alpinejs';

jest.mock('../utilities', () => ({
  navigateTo: jest.fn(),
}));

describe('MappingForm', () => {
  let mappingForm: AlpineComponent<MappingFormComponent>;

  beforeEach(() => {
    mappingForm = MappingForm();
  });

  it('should initialize with correct initial state', () => {
    expect(mappingForm.hasError).toBe(false);
    expect(mappingForm.errorMessage).toBe('');
    expect(mappingForm.name).toBe('');
  });

  it('should set error state and message when name is invalid', () => {
    mappingForm.name = 'Invalid Name';

    mappingForm.createMapping();

    expect(mappingForm.hasError).toBe(true);
    expect(mappingForm.errorMessage).toBe(
      'Name can only contain letters and numbers',
    );
  });

  it('should navigate to create mapping page when name is valid', () => {
    const validName = 'ValidName123';
    mappingForm.name = validName;

    mappingForm.createMapping();

    expect(mappingForm.hasError).toBe(false);
    expect(navigateTo).toHaveBeenCalledWith(
      `${BASE_URL}/column-maps/create?name=${encodeURIComponent(validName)}`,
    );
  });

  it('should reset state and close modal', () => {
    mappingForm.hasError = true;
    mappingForm.errorMessage = 'Error message';
    mappingForm.name = 'Some name';

    mappingForm.closeModal();

    expect(mappingForm.hasError).toBe(false);
    expect(mappingForm.errorMessage).toBe('');
    expect(mappingForm.name).toBe('');
  });
});
