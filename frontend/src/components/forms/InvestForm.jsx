import { useState } from 'react';
import InputField from '../ui/InputField';
import SegmentedControl from '../ui/SegmentedControl';
import styles from '../../styles/PlannerForm.module.css';
import { useFormValidation } from '../../hooks/useFormValidation';

const goals = ['Retirement', 'Child Education', 'Home Purchase', 'Emergency Fund', 'Wealth Creation'];

function InvestForm({ onCalculate }) {
  const [values, setValues] = useState({
    name: '',
    monthly_savings: '',
    age: 30,
    goal: goals[0],
    risk_profile: 'Medium',
  });
  const [errors, setErrors] = useState({});
  const [submitError, setSubmitError] = useState(null);
  const [loading, setLoading] = useState(false);
  const { validate } = useFormValidation({
    name: { required: true },
    monthly_savings: { required: true, min: 0 },
    age: { required: true, min: 18, max: 65 },
  });

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
        monthly_savings: Number(values.monthly_savings),
        risk_profile: values.risk_profile,
        age: Number(values.age),
        goal: values.goal,
      });
    } catch (err) {
      setSubmitError('Could not generate plan. Please retry.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className={styles.panel} onSubmit={handleSubmit}>
      <InputField label="Full Name" name="name" value={values.name} onChange={handleChange} error={errors.name} />
      <InputField
        label="Monthly Savings (₹)"
        name="monthly_savings"
        type="number"
        prefix="₹"
        value={values.monthly_savings}
        onChange={handleChange}
        error={errors.monthly_savings}
      />
      <InputField
        label="Age"
        name="age"
        type="number"
        min={18}
        max={65}
        value={values.age}
        onChange={handleChange}
        error={errors.age}
        helper="18-65"
      />
      <div>
        <label style={{ display: 'block', marginBottom: 8, color: 'var(--text-secondary)' }}>Financial Goal</label>
        <select
          name="goal"
          value={values.goal}
          onChange={handleChange}
          style={{
            width: '100%',
            padding: '12px 14px',
            borderRadius: '12px',
            border: '1px solid var(--border-subtle)',
            background: 'var(--bg-elevated)',
            color: 'var(--text-primary)',
          }}
        >
          {goals.map((g) => (
            <option key={g} value={g}>
              {g}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label style={{ display: 'block', marginBottom: 8, color: 'var(--text-secondary)' }}>Risk Profile</label>
        <SegmentedControl
          options={['Low', 'Medium', 'High']}
          value={values.risk_profile}
          onChange={(val) => setValues((prev) => ({ ...prev, risk_profile: val }))}
        />
      </div>

      {submitError && <div className={styles.error}>{submitError}</div>}

      <div className={styles.actions}>
        <button className={styles.button} type="submit" disabled={loading}>
          {loading && <span className={styles.spinner} aria-hidden />} Plan My Investments
        </button>
      </div>
    </form>
  );
}

export default InvestForm;
