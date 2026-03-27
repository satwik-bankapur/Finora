import { Link } from 'react-router-dom';
import styles from '../styles/Landing.module.css';
import StatCard from '../components/ui/StatCard';
import DonutChart from '../components/charts/DonutChart';
import Badge from '../components/ui/Badge';
import iconTax from '../assets/icon-tax.svg';
import iconInvest from '../assets/icon-invest.svg';
import iconShield from '../assets/icon-shield.svg';

const mockChart = [
  { name: 'Equity MF', value: 52000, percent: 52, color: 'var(--chart-1)' },
  { name: 'Debt/PPF', value: 32000, percent: 32, color: 'var(--chart-2)' },
  { name: 'Gold', value: 16000, percent: 16, color: 'var(--chart-3)' },
];

function Landing() {
  return (
    <div>
      <section className={styles.hero}>
        <div className={styles.eyebrow}>✦ AI-Powered Finance</div>
        <h1 className={styles.heading}>
          Plan <span className={styles.gradient}>Smarter</span>.<br />
          Save More. Live Better.
        </h1>
        <p className={styles.subhead}>
          Finora uses AI to optimize your taxes, guide your investments, and help you build real wealth — designed for India's growing middle class.
        </p>
        <div className={styles.ctaRow}>
          <Link to="/tax" className="btn-primary">Calculate My Tax</Link>
          <Link to="/invest" className={styles.secondary}>Plan My Investments</Link>
        </div>

        <div className={styles.dashboardCard}>
          <div className={styles.dashboardInner}>
            <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: 16, alignItems: 'center' }}>
              <DonutChart data={mockChart} />
              <div style={{ display: 'grid', gap: 10 }}>
                <StatCard icon="💰" label="Monthly Savings" value="₹25,000" />
                <StatCard icon="📈" label="Projected 10Y Corpus" value="₹48,20,000" trend={12} />
                <Badge tone="positive">AI Insights: Add ₹3,000 to ELSS to save ₹45,000 tax</Badge>
              </div>
            </div>
          </div>
        </div>
        <div className={styles.scrollHint}>↓ Scroll to explore</div>
      </section>

      <section id="features" className={styles.features}>
        <h2 className="section-heading">Everything you need to take control</h2>
        <p className="section-subtext">
          Taxes, investments, and wealth tracking in one confident, privacy-first experience.
        </p>
        <div className={styles.featureGrid}>
          {[{
            icon: iconTax,
            title: 'Smart Tax Planner',
            desc: "Calculate your exact tax liability and discover deductions you're missing under 80C, 80D, and more.",
          }, {
            icon: iconInvest,
            title: 'AI Investment Advisor',
            desc: 'Get a personalized portfolio allocation based on your income, risk appetite, and financial goals.',
          }, {
            icon: iconShield,
            title: '100% Private',
            desc: 'All calculations run locally. Your financial data never leaves your device.',
          }].map((f) => (
            <div key={f.title} className={styles.featureCard}>
              <div className={styles.iconWrap}>
                <img src={f.icon} alt="" width={28} height={28} />
              </div>
              <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '18px' }}>{f.title}</h3>
              <p style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section className={styles.how}>
        <h2 className="section-heading">How it works</h2>
        <div className={styles.steps}>
          {[
            { title: 'Enter Your Details', desc: 'Securely add income, deductions, and savings goals.' },
            { title: 'AI Analyzes', desc: 'Our models optimize tax and investments for your profile.' },
            { title: 'Get Your Plan', desc: 'Receive a clear action plan with numbers you can trust.' },
          ].map((step, idx) => (
            <div key={step.title} className={styles.step}>
              <div className={styles.stepNumber}>{idx + 1}</div>
              <div style={{ fontWeight: 700 }}>{step.title}</div>
              <div style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>{step.desc}</div>
            </div>
          ))}
        </div>
      </section>

      <section className={styles.ctaBanner}>
        <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '28px', marginBottom: '12px' }}>
          Ready to take control of your finances?
        </h3>
        <Link to="/tax" className="btn-primary">Start Now</Link>
      </section>
    </div>
  );
}

export default Landing;
