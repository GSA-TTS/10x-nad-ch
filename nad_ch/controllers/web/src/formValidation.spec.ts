import { getMappingTitleValidationError } from './formValidation';

describe('getMappingTitleValidationError', () => {
  test('returns error message if title is empty', () => {
    const result = getMappingTitleValidationError('');
    expect(result).toBe('Mapping name is required');
  });

  test('returns error message if title is longer than 25 characters', () => {
    const longTitle = 'a'.repeat(26);
    const result = getMappingTitleValidationError(longTitle);
    expect(result).toBe('Enter less than 25 letters or numbers');
  });

  test('returns errormessage  if title contains invalid characters', () => {
    const invalidTitle = 'test@123';
    const result = getMappingTitleValidationError(invalidTitle);
    expect(result).toBe('Name can only contain letters and numbers');
  });

  test('returns null for a valid title', () => {
    const validTitle = 'ValidTitle123';
    const result = getMappingTitleValidationError(validTitle);
    expect(result).toBeNull();
  });
});
