import { AlpineComponent } from 'alpinejs';
import { BASE_URL } from '../config';
import { getMappingNameValidationError } from '../formValidation';
import { navigateTo } from '../utilities';

export interface MappingFormComponent {
  hasError: boolean;
  errorMessage: string;
  name: string;
  createMapping: () => void;
  closeModal: () => void;
}

export function MappingForm(): AlpineComponent<MappingFormComponent> {
  return {
    hasError: false,
    errorMessage: '',
    name: '',
    createMapping(): void {
      this.hasError = false;

      const validationError = getMappingNameValidationError(this.name);

      if (validationError) {
        this.hasError = true;
        this.errorMessage = validationError;
      } else {
        navigateTo(
          `${BASE_URL}/column-maps/create?name=${encodeURIComponent(this.name)}`,
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
