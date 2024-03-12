export default function MappingForm() {
  return {
    hasError: false,
    errorMessage: "",
    title: "",
    createMapping(): void {
      this.hasError = false;

      const validationError: string | null =
        this.title === ""
          ? "Mapping name is required"
          : this.title.length > 25
          ? "Enter less than 25 letters or numbers"
          : /[^a-zA-Z0-9]/.test(this.title)
          ? "Name can only contain letters and numbers"
          : null;

      if (validationError) {
        this.hasError = true;
        this.errorMessage = validationError;
      } else {
        const baseUrl: string = window.Alpine.store("config").BASE_URL;
        const url: string = `${baseUrl}/mappings/create?title=${encodeURIComponent(
          this.title
        )}`;
        window.location.href = url;
      }
    },
    closeModal(): void {
      this.title = "";
      this.hasError = false;
      this.errorMessage = "";
      const button: HTMLElement | null =
        document.getElementById("cancel-button");
      if (button) {
        button.setAttribute("data-close-modal", "");
        button.click();
      }
    },
  };
}
