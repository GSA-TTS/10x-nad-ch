import "@uswds/uswds/css/uswds.css";
import "@uswds/uswds";
import Alpine from "alpinejs";

declare global {
  interface Window {
    Alpine: any;
  }
}

window.Alpine = Alpine;

Alpine.store("config", {
  BASE_URL: "http://localhost:8080",
});

Alpine.start();
