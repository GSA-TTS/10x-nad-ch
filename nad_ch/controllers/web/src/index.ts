import '@uswds/uswds/css/uswds.css';
import '@uswds/uswds';
import Alpine from 'alpinejs';
import MappingForm from './components/MappingForm';

declare global {
  interface Window {
    Alpine: any;
  }
}

document.addEventListener('alpine:init', () => {
  Alpine.data('MappingForm', MappingForm);
});

window.Alpine = Alpine;

Alpine.start();
