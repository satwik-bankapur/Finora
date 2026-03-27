import styles from '../../styles/Tooltip.module.css';

function Tooltip({ content, className }) {
  return (
    <span className={`${styles.trigger} ${className || ''}`} tabIndex={0} aria-label={content}>
      ⓘ
      <span className={styles.bubble}>{content}</span>
    </span>
  );
}

export default Tooltip;
