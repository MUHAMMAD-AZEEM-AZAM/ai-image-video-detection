import React from 'react';
import styles from './Navbar.module.css'; // Import CSS module
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className={styles.navbar}>
      <div ></div>
      <div className={styles['nav-links']}>
        <Link to="/" className={styles['nav-link']}>Home</Link>
        <Link to="/about" className={styles['nav-link']}>About</Link>
      </div>
    </nav>
  );
};

export default Navbar;
