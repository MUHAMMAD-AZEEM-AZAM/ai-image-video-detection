import React from 'react';
import PropTypes from 'prop-types';

const CustomButton = ({ loading, disabled, onClick, children }) => {
  return (
    <button       className={`button ${disabled || loading ? 'button-disabled' : ''}`}
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