import React from 'react';

const InputField = ({ value, onChange, placeholder }) => (
  <input
    type="text"
    value={value}
    onChange={onChange}
    placeholder={placeholder}
    style={{
      backgroundColor: '#000000',
      flex: 1,
      padding: '8px',
      marginRight: '10px',
      fontSize: '14px',
      borderWidth: '1px' }}
  />
);

export default InputField;
