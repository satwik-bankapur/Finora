import styles from '../../styles/SegmentedControl.module.css';

const descriptors = {
  Low: 'Stable returns, capital safety',
  Medium: 'Balanced growth',
  High: 'Aggressive growth',
};

function SegmentedControl({ options, value, onChange }) {
  return (
    <div>
      <div className={styles.wrapper}>
        {options.map((opt) => (
          <button
            key={opt}
            type="button"
            className={`${styles.option} ${value === opt ? styles.active : ''}`}
            onClick={() => onChange(opt)}
          >
            {opt}
          </button>
        ))}
      </div>
      {value && descriptors[value] && <div className={styles.descriptor}>{descriptors[value]}</div>}
    </div>
  );
}

export default SegmentedControl;
