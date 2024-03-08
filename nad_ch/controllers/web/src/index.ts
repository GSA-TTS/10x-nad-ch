import "@uswds/uswds/css/uswds.css";
import Alpine from "alpinejs";

declare global {
  interface Window {
    Alpine: any;
  }
}

window.Alpine = Alpine;

Alpine.start();
