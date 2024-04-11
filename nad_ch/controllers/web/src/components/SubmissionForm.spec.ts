/**
 * @jest-environment jsdom
 */

import { SubmissionForm, SubmissionFormComponent } from './SubmissionForm';
import { BASE_URL } from '../config';
import { navigateTo } from '../utilities';
import { AlpineComponent } from 'alpinejs';

jest.mock('../utilities', () => ({
  navigateTo: jest.fn(),
}));

describe('MappingForm', () => {
  let submissionForm: AlpineComponent<SubmissionFormComponent>;

  beforeEach(() => {
    submissionForm = SubmissionForm();
  });

  it('should initialize with correct initial state', () => {
    expect(submissionForm.hasError).toBe(false);
    expect(submissionForm.errorMessage).toBe('');
    expect(submissionForm.name).toBe('');
  });

  it('should set error state and message when name is invalid', () => {
    submissionForm.name = 'Invalid Name';

    submissionForm.create();

    expect(submissionForm.hasError).toBe(true);
    expect(submissionForm.errorMessage).toBe(
      'Name can only contain letters and numbers',
    );
  });

  it('should navigate to create mapping page when name is valid', () => {
    const validName = 'ValidName123';
    submissionForm.name = validName;

    submissionForm.create();

    expect(submissionForm.hasError).toBe(false);
    expect(navigateTo).toHaveBeenCalledWith(
      `${BASE_URL}/data-submissions/create?name=${encodeURIComponent(validName)}`,
    );
  });

  it('should reset state and close modal', () => {
    submissionForm.hasError = true;
    submissionForm.errorMessage = 'Error message';
    submissionForm.name = 'Some name';

    submissionForm.closeModal();

    expect(submissionForm.hasError).toBe(false);
    expect(submissionForm.errorMessage).toBe('');
    expect(submissionForm.name).toBe('');
  });
});
