import "@uswds/uswds/css/uswds.css";
import "@uswds/uswds";
import Alpine from "alpinejs";
import MappingForm from "./components/MappingForm";

declare global {
  interface Window {
    Alpine: any;
  }
}

document.addEventListener("alpine:init", () => {
  Alpine.data("MappingForm", MappingForm);
});

Alpine.store("config", {
  BASE_URL: "http://localhost:8080",
});

window.Alpine = Alpine;

Alpine.start();
