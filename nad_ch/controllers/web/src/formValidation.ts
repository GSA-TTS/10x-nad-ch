export function getMappingTitleValidationError(title: string): string | null {
  if (title === '') {
    return 'Mapping name is required';
  } else if (title.length > 25) {
    return 'Enter less than 25 letters or numbers';
  } else if (/[^a-zA-Z0-9]/.test(title)) {
    return 'Name can only contain letters and numbers';
  }
  return null;
}
