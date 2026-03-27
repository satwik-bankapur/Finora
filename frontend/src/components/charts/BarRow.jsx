import { useEffect, useState } from 'react';
import styles from '../../styles/BarRow.module.css';
import { formatCurrency } from '../../utils/formatCurrency';

function BarRow({ label, value, percent, color }) {
  const [width, setWidth] = useState('0%');
  useEffect(() => {
    const timer = setTimeout(() => setWidth(`${percent}%`), 60);
    return () => clearTimeout(timer);
  }, [percent]);

  return (
    <div className={styles.row}>
      <div>{label}</div>
      <div className={styles.barOuter}>
        <div className={styles.barInner} style={{ width, background: color }} />
      </div>
      <div className={styles.amount}>{formatCurrency(value)}</div>
    </div>
  );
}

export default BarRow;
