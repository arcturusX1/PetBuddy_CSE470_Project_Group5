import React, { useState } from 'react';
import FormTest from './components/FormTest';

const FormTestContainer = () => {
  const [formData, setFormData] = useState({
    username: '',
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    password: '',
    confirm_password: '',
    is_vet: false
  });
  
  const [errors, setErrors] = useState({});
  const [status, setStatus] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: type === 'checkbox' ? checked : value
    }));
    // Clear error when field is edited
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: null }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;
    
    if (!formData.username) newErrors.username = ['Username is required'];
    if (!formData.first_name) newErrors.first_name = ['First name is required'];
    if (!formData.last_name) newErrors.last_name = ['Last name is required'];
    
    if (!formData.email) {
      newErrors.email = ['Email is required'];
    } else if (!emailRegex.test(formData.email)) {
      newErrors.email = ['Please enter a valid email address'];
    }
    
    if (!formData.phone) newErrors.phone = ['Phone is required'];
    
    if (!formData.password) {
      newErrors.password = ['Password is required'];
    } else if (!passwordRegex.test(formData.password)) {
      newErrors.password = ['Password must be at least 8 characters long and contain letters and numbers'];
    }
    
    if (formData.password !== formData.confirm_password) {
      newErrors.confirm_password = ['Passwords do not match'];
    }

    return newErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setStatus('Submitting...');

    const formErrors = validateForm();
    if (Object.keys(formErrors).length > 0) {
      setErrors(formErrors);
      setStatus('Please fix the errors above');
      setIsLoading(false);
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/api/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (response.ok) {
        setStatus('Registration successful!');
        setFormData({
          username: '',
          first_name: '',
          last_name: '',
          email: '',
          phone: '',
          password: '',
          confirm_password: '',
          is_vet: false
        });
        setErrors({});
      } else {
        setStatus('Registration failed');
        if (data.errors) {
          setErrors(data.errors);
        }
      }
    } catch (error) {
      setStatus('Error submitting form. Please try again.');
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <FormTest
      formData={formData}
      errors={errors}
      status={status}
      isLoading={isLoading}
      onSubmit={handleSubmit}
      onChange={handleChange}
    />
  );
};

export default FormTestContainer;