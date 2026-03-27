import { useMemo, useState } from 'react';
import PageHeader from '../components/layout/PageHeader';
import InvestForm from '../components/forms/InvestForm';
import DonutChart from '../components/charts/DonutChart';
import StatCard from '../components/ui/StatCard';
import styles from '../styles/InvestPlanner.module.css';
import Skeleton from '../components/ui/Skeleton';
import { postInvest } from '../api/finora';
import { formatCurrency, formatPercent } from '../utils/formatCurrency';
import { useCountUp } from '../hooks/useCountUp';

const fallbackAllocation = [
  { name: 'Equity MF', percent: 50, value: 12000, color: 'var(--chart-1)' },
  { name: 'Debt/PPF', percent: 30, value: 7200, color: 'var(--chart-2)' },
  { name: 'Gold', percent: 20, value: 4800, color: 'var(--chart-3)' },
];

function InvestPlanner() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleCalculate = async (payload) => {
    setLoading(true);
    setError(null);
    try {
      const { data } = await postInvest(payload);
      setResults(data);
      return data;
    } catch (err) {
      setError('Unable to generate your investment plan. Please retry.');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const allocation = useMemo(() => {
    const portfolio = results?.portfolio;
    const baseColors = ['var(--chart-1)', 'var(--chart-2)', 'var(--chart-3)', 'var(--chart-4)', 'var(--chart-5)'];

    if (!portfolio) return fallbackAllocation;

    return Object.entries(portfolio).map(([name, info], idx) => ({
      name,
      percent: Number(String(info.percentage).replace('%', '')) || 0,
      value: info.monthly_amount || 0,
      color: baseColors[idx % baseColors.length],
    }));
  }, [results]);

  const projectedCorpus = useCountUp(results?.estimated_returns?.total_future_value || 0);
  const monthlySavings = results?.monthly_savings || 0;
  const years = results?.years || 10;
  const avgReturn = results?.avg_return || 12;

  return (
    <div>
      <PageHeader
        title="Investment Planner"
        subtitle="AI-crafted allocations and projections tuned to your risk profile."
        breadcrumb="Home / Investment Planner"
      />

      <div className={styles.layout}>
        <InvestForm onCalculate={handleCalculate} />

        <div className={styles.results}>
          {!results && !loading && !error && (
            <div style={{ textAlign: 'center', color: 'var(--text-secondary)' }}>
              Run the planner to see your personalized portfolio.
            </div>
          )}

          {error && <div style={{ color: 'var(--negative)' }}>{error}</div>}

          {loading && (
            <div style={{ display: 'grid', gap: 10 }}>
              <Skeleton height={20} width="60%" />
              <Skeleton height={200} />
              <Skeleton height={20} width="80%" />
              <Skeleton height={120} />
            </div>
          )}

          {(!loading && (results || fallbackAllocation)) && (
            <>
              <h3 style={{ fontFamily: 'var(--font-display)' }}>Portfolio Allocation</h3>
              <DonutChart data={allocation} />

              <StatCard
                icon="🎯"
                label={`Projected Corpus After ${years} Years`}
                value={formatCurrency(projectedCorpus)}
                trend={avgReturn}
              />
              <div style={{ color: 'var(--text-secondary)' }}>
                Based on {formatCurrency(monthlySavings)} per month at {formatPercent(avgReturn)} average annual returns.
              </div>
              <div className={styles.progressBar}>
                <div className={styles.progressFill} style={{ width: `${Math.min((results?.age || 30) / 65 * 100, 100)}%` }} />
              </div>

              <div className={styles.allocationGrid}>
                {allocation.map((item) => (
                  <div key={item.name} className={styles.assetCard} style={{ borderLeft: `4px solid ${item.color}` }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <div style={{ fontWeight: 700 }}>{item.name}</div>
                      <span style={{ color: 'var(--text-secondary)', fontFamily: 'var(--font-mono)' }}>{item.percent}%</span>
                    </div>
                    <div style={{ color: 'var(--text-secondary)', fontFamily: 'var(--font-mono)' }}>{formatCurrency(item.value)}</div>
                    <div style={{ color: 'var(--text-muted)', fontSize: '13px' }}>AI note: optimized for your risk profile.</div>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default InvestPlanner;
