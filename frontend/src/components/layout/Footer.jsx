import { Link } from 'react-router-dom';
import styles from '../../styles/Footer.module.css';

function Footer() {
  return (
    <footer className={styles.footer}>
      <div className={styles.logo}>
        <span aria-hidden>◆</span>
        Finora
      </div>
      <div className={styles.links}>
        <Link to="/tax">Tax Planner</Link>
        <Link to="/invest">Invest Planner</Link>
      </div>
      <div>Made with ♥ for India</div>
    </footer>
  );
}

export default Footer;
