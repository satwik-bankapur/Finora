import { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import styles from '../../styles/Navbar.module.css';
import mark from '../../assets/finora-mark.svg';

const navItems = [
  { to: '/#features', label: 'Features' },
  { to: '/tax', label: 'Tax Planner' },
  { to: '/invest', label: 'Invest Planner' },
];

function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 80);
    onScroll();
    window.addEventListener('scroll', onScroll);
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  useEffect(() => {
    setOpen(false);
  }, [location.pathname]);

  return (
    <nav className={`${styles.nav} ${scrolled ? styles.navScrolled : ''}`}>
      <Link to="/" className={styles.brand} aria-label="Finora home">
        <img src={mark} alt="Finora logo" className={styles.logoIcon} />
        Finora
      </Link>

      <div className={styles.links}>
        {navItems.map((item) => (
          <Link key={item.label} to={item.to} className={styles.link}>
            {item.label}
          </Link>
        ))}
      </div>

      <Link to="/tax" className={styles.ctaGhost}>
        Get Started
      </Link>

      <button
        className={styles.mobileToggle}
        aria-label="Toggle navigation"
        onClick={() => setOpen((v) => !v)}
      >
        ☰
      </button>

      {open && (
        <div className={styles.mobileMenu}>
          <div className={styles.mobileLinks}>
            {navItems.map((item) => (
              <Link key={item.label} to={item.to} className={styles.link}>
                {item.label}
              </Link>
            ))}
            <Link to="/tax" className={styles.ctaGhost}>
              Get Started
            </Link>
          </div>
        </div>
      )}
    </nav>
  );
}

export default Navbar;
