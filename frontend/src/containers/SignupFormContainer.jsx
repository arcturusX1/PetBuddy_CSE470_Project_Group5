import React, { useState, useEffect } from 'react';
import SignupFormPresentation from '../components/SignupFormPresentation';
const SignupForm = () => {
    const [formData, setFormData] = useState({
        data_text: '',
        data_bool: '',
        data_int: ''
    })

    const [status, setStatus] = useState('');
    const [errors, setErrors] = useState({});
    const [isLoading, setIsLoading] = useState(false);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prevData => ({
            ...prevData,
            [name]: value
        }));
    };
    const validateForm = () => {
        const newErrors = {};
        if (!formData.data_text) newErrors.data_text = ['missing'];
        if (!formData.data_bool) newErrors.data_bool = ['missing'];
        if (!formData.data_int) newErrors.data_int = ['missing'];

        return newErrors;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);

        const formErrors = validateForm();
        if (Object.keys(formErrors).length > 0) {
            setErrors(formErrors);
            setIsLoading(false);
            return;
        }

        try {
            const response = await fetch('http://localhost:5000/api/form_test', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            const data = await response.json();
            if (response.ok) {
                setStatus('Sucess')
                alert(status, data)
                setFormData({
                    data_text: '',
                    data_bool: '',
                    data_int: ''
                });
                setErrors({});
            }
            else {
                setStatus('Errors')
                setErrors(data.errors);
                alert(status, errors)
            };
        }
        catch (error) {
            setStatus('error submitting')
            alert(status, error)
        }
        finally {
            setIsLoading(false);
        }
    }
    console.log('SignupForm state before render:', { formData, errors, status, isLoading });
    return (
        <SignupFormPresentation
            formData={formData}
            errors={errors}
            status={status}
            isLoading={isLoading}
            onSubmit={handleSubmit}
            onChange={handleChange}
        />
    )
};

export default SignupForm;

