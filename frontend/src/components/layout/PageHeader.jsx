import styles from '../../styles/PageHeader.module.css';

function PageHeader({ title, subtitle, breadcrumb }) {
  return (
    <div className={styles.wrapper}>
      {breadcrumb && <div className={styles.breadcrumb}>{breadcrumb}</div>}
      <h1 className={styles.title}>{title}</h1>
      {subtitle && <p className={styles.subtitle}>{subtitle}</p>}
    </div>
  );
}

export default PageHeader;
