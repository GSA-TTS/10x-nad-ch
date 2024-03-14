export function getMappingNameValidationError(name: string): string | null {
  if (name === '') {
    return 'Mapping name is required';
  } else if (name.length > 25) {
    return 'Enter less than 25 letters or numbers';
  } else if (/[^a-zA-Z0-9]/.test(name)) {
    return 'Name can only contain letters and numbers';
  }
  return null;
}
