import { AlpineComponent } from 'alpinejs';
import { BASE_URL } from '../config';
import { getMappingNameValidationError } from '../formValidation';
import { navigateTo } from '../utilities';

export interface SubmissionFormComponent {
  hasError: boolean;
  errorMessage: string;
  name: string;
  create: () => void;
  closeModal: () => void;
}

export function SubmissionForm(): AlpineComponent<SubmissionFormComponent> {
  return {
    hasError: false,
    errorMessage: '',
    name: '',
    create(): void {
      this.hasError = false;

      const validationError = getMappingNameValidationError(this.name);

      if (validationError) {
        this.hasError = true;
        this.errorMessage = validationError;
      } else {
        navigateTo(
          `${BASE_URL}/data-submissions/create?name=${encodeURIComponent(this.name)}`,
        );
      }
    },
    closeModal(): void {
      this.name = '';
      this.hasError = false;
      this.errorMessage = '';
      const button: HTMLElement | null =
        document.getElementById('cancel-button');
      if (button) {
        button.setAttribute('data-close-modal', '');
        button.click();
      }
    },
  };
}
