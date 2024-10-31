import React from 'react';
import FormField from './FormField';


const FormTest = ({
  formData,
  errors,
  status,
  isLoading,
  onSubmit,
  onChange
}) => {
  return (
    <div className="max-w-md mx-auto p-6">
      <h2 className="text-2xl font-bold mb-6">User Registration</h2>
      <form onSubmit={onSubmit} className="space-y-4">
        <FormField
          label="Username"
          type="text"
          name="username"
          value={formData.username}
          onChange={onChange}
          error={errors.username}
        />

        <FormField
          label="First Name"
          type="text"
          name="first_name"
          value={formData.first_name}
          onChange={onChange}
          error={errors.first_name}
        />

        <FormField
          label="Last Name"
          type="text"
          name="last_name"
          value={formData.last_name}
          onChange={onChange}
          error={errors.last_name}
        />

        <FormField
          label="Email"
          type="email"
          name="email"
          value={formData.email}
          onChange={onChange}
          error={errors.email}
        />

        <FormField
          label="Phone"
          type="tel"
          name="phone"
          value={formData.phone}
          onChange={onChange}
          error={errors.phone}
        />

        <FormField
          label="Password"
          type="password"
          name="password"
          value={formData.password}
          onChange={onChange}
          error={errors.password}
        />

        <FormField
          label="Confirm Password"
          type="password"
          name="confirm_password"
          value={formData.confirm_password}
          onChange={onChange}
          error={errors.confirm_password}
        />

        <div className="flex items-center">
          <input
            type="checkbox"
            id="is_vet"
            name="is_vet"
            checked={formData.is_vet}
            onChange={onChange}
            className="mr-2"
          />
          <label htmlFor="is_vet" className="text-sm font-medium">
            Register as Veterinarian
          </label>
        </div>

        <button 
          type="submit"
          disabled={isLoading}
          className={`w-full ${isLoading ? 'bg-gray-400' : 'bg-blue-500 hover:bg-blue-600'} 
            text-white p-2 rounded`}
        >
          {isLoading ? 'Registering...' : 'Register'}
        </button>

        {status && (
          <p className={`text-center ${
            status.includes('successful') ? 'text-green-500' : 'text-red-500'
          }`}>
            {status}
          </p>
        )}
      </form>
    </div>
  );
};

export default FormTest;