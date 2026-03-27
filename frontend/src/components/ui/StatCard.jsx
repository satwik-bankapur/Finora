import styles from '../../styles/StatCard.module.css';
import Badge from './Badge';

function StatCard({ icon, label, value, trend }) {
  return (
    <div className={`${styles.card} card`}> 
      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        <span aria-hidden>{icon}</span>
        <span className={styles.label}>{label}</span>
        {trend && <Badge tone={trend > 0 ? 'positive' : 'negative'}>{trend > 0 ? `▲ ${trend}%` : `▼ ${Math.abs(trend)}%`}</Badge>}
      </div>
      <div className={styles.value}>{value}</div>
    </div>
  );
}

export default StatCard;
