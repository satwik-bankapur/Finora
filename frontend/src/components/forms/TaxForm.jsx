import { useMemo, useState } from 'react';
import InputField from '../ui/InputField';
import styles from '../../styles/PlannerForm.module.css';
import { useFormValidation } from '../../hooks/useFormValidation';
import { formatCurrency } from '../../utils/formatCurrency';

function TaxForm({ onCalculate }) {
  const [values, setValues] = useState({
    name: '',
    annual_income: '',
    ELSS: '',
    PPF: '',
    health_insurance: '',
  });
  const [errors, setErrors] = useState({});
  const [submitError, setSubmitError] = useState(null);
  const [loading, setLoading] = useState(false);
  const { validate } = useFormValidation({
    name: { required: true },
    annual_income: { required: true, min: 0 },
  });

  const deductions = useMemo(() => {
    const total = Number(values.ELSS || 0) + Number(values.PPF || 0) + Number(values.health_insurance || 0);
    return total;
  }, [values]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setValues((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const nextErrors = validate(values);
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length) return;
    setSubmitError(null);
    setLoading(true);
    try {
      await onCalculate({
        name: values.name,
        annual_income: Number(values.annual_income),
        investments: {
          ELSS: Number(values.ELSS || 0),
          PPF: Number(values.PPF || 0),
          health_insurance: Number(values.health_insurance || 0),
        },
      });
    } catch (err) {
      setSubmitError('Could not calculate tax. Please retry.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className={styles.panel} onSubmit={handleSubmit}>
      <InputField
        label="Full Name"
        name="name"
        value={values.name}
        onChange={handleChange}
        error={errors.name}
      />
      <InputField
        label="Annual Income (₹)"
        name="annual_income"
        type="number"
        value={values.annual_income}
        onChange={handleChange}
        prefix="₹"
        error={errors.annual_income}
      />
      <InputField
        label="ELSS Investment (₹)"
        name="ELSS"
        type="number"
        value={values.ELSS}
        onChange={handleChange}
        prefix="₹"
        tooltip="Equity Linked Savings Scheme — up to ₹1.5L deductible"
      />
      <InputField
        label="PPF Investment (₹)"
        name="PPF"
        type="number"
        value={values.PPF}
        onChange={handleChange}
        prefix="₹"
        tooltip="Public Provident Fund — long-term, tax-saving"
      />
      <InputField
        label="Health Insurance Premium (₹)"
        name="health_insurance"
        type="number"
        value={values.health_insurance}
        onChange={handleChange}
        prefix="₹"
        tooltip="Section 80D deduction for medical insurance"
      />

      <div className={styles.deductions}>Total Deductions: {formatCurrency(deductions)}</div>

      {submitError && <div className={styles.error}>{submitError}</div>}

      <div className={styles.actions}>
        <button className={styles.button} type="submit" disabled={loading}>
          {loading && <span className={styles.spinner} aria-hidden />} Calculate Tax
        </button>
      </div>
    </form>
  );
}

export default TaxForm;
