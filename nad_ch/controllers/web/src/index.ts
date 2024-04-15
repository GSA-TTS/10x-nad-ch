import '@uswds/uswds/css/uswds.css';
import '@uswds/uswds';
import Alpine from 'alpinejs';
import { MappingForm } from './components/MappingForm';
import { CompletenessReport } from './components/CompletenessReport';

declare global {
  interface Window {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    Alpine: any;
  }
}

document.addEventListener('alpine:init', () => {
  Alpine.data('MappingForm', MappingForm);
  Alpine.data('CompletenessReport', CompletenessReport);
});

window.Alpine = Alpine;

Alpine.start();
