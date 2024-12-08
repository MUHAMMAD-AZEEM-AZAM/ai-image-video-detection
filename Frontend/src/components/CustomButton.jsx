import React from 'react';
import PropTypes from 'prop-types';

const CustomButton = ({ loading, disabled, onClick, children }) => {
  return (
    <button style={{maxWidth:'140px'}} className={`button ${disabled || loading ? 'button-disabled' : ''}`}
    onClick={onClick} disabled={disabled || loading}>
      {loading ? 'Processing...' : children}
    </button>
  );
};

CustomButton.propTypes = {
  loading: PropTypes.bool,
  disabled: PropTypes.bool,
  onClick: PropTypes.func.isRequired,
  children: PropTypes.node.isRequired,
};



export default CustomButton;