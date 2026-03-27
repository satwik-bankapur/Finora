export function useFormValidation(rules) {
  const validate = (values) => {
    const errors = {};
    Object.entries(rules).forEach(([field, rule]) => {
      const value = values[field];
      if (rule.required && (value === '' || value === null || value === undefined)) {
        errors[field] = 'Required';
        return;
      }
      if (rule.min !== undefined && Number(value) < rule.min) {
        errors[field] = `Must be at least ${rule.min}`;
      }
      if (rule.max !== undefined && Number(value) > rule.max) {
        errors[field] = `Must be ≤ ${rule.max}`;
      }
    });
    return errors;
  };
  return { validate };
}
