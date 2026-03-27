import { useEffect, useMemo, useState } from 'react';
import styles from '../../styles/DonutChart.module.css';
import { formatCurrency } from '../../utils/formatCurrency';

const SIZE = 240;
const STROKE = 18;

function DonutChart({ data }) {
  const [animate, setAnimate] = useState(false);
  const radius = (SIZE - STROKE) / 2;
  const circumference = 2 * Math.PI * radius;
  const total = useMemo(() => data.reduce((acc, item) => acc + item.value, 0), [data]);

  useEffect(() => {
    setAnimate(false);
    const timer = setTimeout(() => setAnimate(true), 50);
    return () => clearTimeout(timer);
  }, [data]);

  let offset = 0;

  return (
    <div className={styles.chartWrap}>
      <svg width={SIZE} height={SIZE} viewBox={`0 0 ${SIZE} ${SIZE}`}>
        <g transform={`rotate(-90 ${SIZE / 2} ${SIZE / 2})`}>
          {data.map((slice) => {
            const percent = total ? slice.value / total : 0;
            const dash = percent * circumference;
            const circle = (
              <circle
                key={slice.name}
                cx={SIZE / 2}
                cy={SIZE / 2}
                r={radius}
                fill="transparent"
                stroke={slice.color}
                strokeWidth={STROKE}
                strokeDasharray={`${dash} ${circumference}`}
                strokeDashoffset={animate ? -offset : circumference}
                strokeLinecap="round"
                style={{ transition: 'stroke-dashoffset 0.9s ease' }}
              />
            );
            offset += dash;
            return circle;
          })}
        </g>
        <circle
          cx={SIZE / 2}
          cy={SIZE / 2}
          r={radius - STROKE}
          fill="var(--bg-base)"
        />
        <text
          x="50%"
          y="50%"
          textAnchor="middle"
          dominantBaseline="middle"
          fill="var(--text-primary)"
          style={{ fontFamily: 'var(--font-mono)', fontSize: '18px' }}
        >
          {formatCurrency(total)}
        </text>
      </svg>

      <div className={styles.legend}>
        {data.map((item) => (
          <div key={item.name} className={styles.legendItem}>
            <div className={styles.legendLeft}>
              <span className={styles.dot} style={{ background: item.color }} />
              <div>
                <div>{item.name}</div>
                <div className={styles.amount}>{item.percent}%</div>
              </div>
            </div>
            <div className={styles.amount}>{formatCurrency(item.value)}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default DonutChart;
