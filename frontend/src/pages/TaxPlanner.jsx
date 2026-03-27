import { useState } from 'react';
import PageHeader from '../components/layout/PageHeader';
import TaxForm from '../components/forms/TaxForm';
import StatCard from '../components/ui/StatCard';
import BarRow from '../components/charts/BarRow';
import Skeleton from '../components/ui/Skeleton';
import styles from '../styles/TaxPlanner.module.css';
import { postTax } from '../api/finora';
import { formatCurrency, formatPercent } from '../utils/formatCurrency';
import { useCountUp } from '../hooks/useCountUp';

function TaxPlanner() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleCalculate = async (payload) => {
    setLoading(true);
    setError(null);
    try {
      const { data } = await postTax(payload);
      setResults(data);
      return data;
    } catch (err) {
      setError('Something went wrong while calculating your tax. Please try again.');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const grossIncome = useCountUp(results?.annual_income || 0);
  const deductions = useCountUp(results?.total_deductions || 0);
  const taxBefore = useCountUp(results?.tax_before_deductions || results?.tax_before_planning || 0);
  const taxAfter = useCountUp(results?.tax_after_deductions || results?.tax_after_planning || 0);
  const taxSaved = useCountUp(
    results?.tax_saved ||
      (results ? (results.tax_before_deductions || 0) - (results.tax_after_deductions || 0) : 0)
  );

  const breakdown = Object.entries(results?.deductions || {}).map(([label, value], idx) => ({
    label,
    value,
    percent: results?.total_deductions ? Math.round((value / results.total_deductions) * 100) : 0,
    color: [`var(--chart-1)`, `var(--chart-2)`, `var(--chart-3)`, `var(--chart-4)`, `var(--chart-5)`][idx % 5],
  }));

  return (
    <div>
      <PageHeader
        title="Tax Planner"
        subtitle="Calculate your exact tax liability and uncover every deduction you deserve."
        breadcrumb="Home / Tax Planner"
      />

      <div className={styles.layout}>
        <TaxForm onCalculate={handleCalculate} />

        <div className={styles.resultsCard}>
          {!results && !loading && !error && (
            <div className={styles.placeholder}>
              <div style={{ width: 120, height: 80, borderRadius: 16, border: '1px dashed var(--border-subtle)' }} />
              <div>Fill in your details to see your tax breakdown</div>
            </div>
          )}

          {loading && (
            <div className={styles.statGrid}>
              {Array.from({ length: 4 }).map((_, idx) => (
                <div key={idx} className="card" style={{ padding: 16 }}>
                  <Skeleton height={14} width="40%" />
                  <Skeleton height={24} width="80%" />
                </div>
              ))}
            </div>
          )}

          {error && <div className="card" style={{ padding: 12, color: 'var(--negative)' }}>{error}</div>}

          {results && !loading && (
            <>
              <div className={styles.statGrid}>
                <StatCard icon="💼" label="Annual Income" value={formatCurrency(grossIncome)} />
                <StatCard icon="🧾" label="Total Deductions" value={formatCurrency(deductions)} />
                <StatCard icon="📉" label="Tax Before Planning" value={formatCurrency(taxBefore)} />
                <StatCard icon="✅" label="Tax After Planning" value={formatCurrency(taxAfter)} />
              </div>

              <div className={styles.heroSave}>
                <div style={{ color: 'var(--positive)', fontFamily: 'var(--font-display)', fontSize: '32px' }}>
                  You save {formatCurrency(taxSaved)} in taxes 🎉
                </div>
                <div style={{ color: 'var(--text-secondary)' }}>
                  That is {formatPercent((results?.tax_saved || taxSaved) / Math.max(results?.annual_income || 1, 1) * 100)} of your gross income back in your pocket
                </div>
              </div>

              <div className="card" style={{ padding: 16 }}>
                <h3 style={{ marginBottom: 10 }}>Deductions Breakdown</h3>
                <div className={styles.breakdown}>
                  {breakdown.length ? (
                    breakdown.map((item) => (
                      <BarRow key={item.label} {...item} />
                    ))
                  ) : (
                    <div style={{ color: 'var(--text-secondary)' }}>No deductions captured yet.</div>
                  )}
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default TaxPlanner;
