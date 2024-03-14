import { getMappingNameValidationError } from './formValidation';

describe('getMappingNameValidationError', () => {
  test('returns error message if name is empty', () => {
    const result = getMappingNameValidationError('');
    expect(result).toBe('Mapping name is required');
  });

  test('returns error message if name is longer than 25 characters', () => {
    const longName = 'a'.repeat(26);
    const result = getMappingNameValidationError(longName);
    expect(result).toBe('Enter less than 25 letters or numbers');
  });

  test('returns errormessage  if name contains invalid characters', () => {
    const invalidName = 'test@123';
    const result = getMappingNameValidationError(invalidName);
    expect(result).toBe('Name can only contain letters and numbers');
  });

  test('returns null for a valid name', () => {
    const validName = 'ValidName123';
    const result = getMappingNameValidationError(validName);
    expect(result).toBeNull();
  });
});
