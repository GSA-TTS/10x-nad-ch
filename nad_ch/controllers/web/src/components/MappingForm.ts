import { BASE_URL } from '../config';
import { getMappingTitleValidationError } from '../formValidation';
import { navigateTo } from '../utilities';

export default function MappingForm() {
  return {
    hasError: false,
    errorMessage: '',
    title: '',
    createMapping(): void {
      this.hasError = false;

      const validationError = getMappingTitleValidationError(this.title);

      if (validationError) {
        this.hasError = true;
        this.errorMessage = validationError;
      } else {
        navigateTo(
          `${BASE_URL}/mappings/create?title=${encodeURIComponent(this.title)}`,
        );
      }
    },
    closeModal(): void {
      this.title = '';
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
