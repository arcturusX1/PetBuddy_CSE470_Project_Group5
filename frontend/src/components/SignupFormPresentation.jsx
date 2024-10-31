import React from 'react';

const SignupFormPresentation = ({ formData, errors, status, isLoading, onSubmit, onChange }) => {
    console.log('Props received:', { formData, errors, status, isLoading });
    return (
        <div className="signup-form">
            <h2>Sign Up</h2>
            <form onSubmit={onSubmit}>
                <div className="form-group">
                    <label htmlFor="data_text">Text Data:</label>
                    <input
                        type="text"
                        id="data_text"
                        name="data_text"
                        value={formData.data_text}
                        onChange={onChange}
                    />
                    {errors.data_text && <p className="error">{errors.data_text[0]}</p>}
                </div>

                <div className="form-group">
                    <label htmlFor="data_bool">Boolean Data:</label>
                    <select
                        id="data_bool"
                        name="data_bool"
                        value={formData.data_bool}
                        onChange={onChange}
                    >
                        <option value="">Select</option>
                        <option value="true">True</option>
                        <option value="false">False</option>
                    </select>
                    {errors.data_bool && <p className="error">{errors.data_bool[0]}</p>}
                </div>

                <div className="form-group">
                    <label htmlFor="data_int">Integer Data:</label>
                    <input
                        type="number"
                        id="data_int"
                        name="data_int"
                        value={formData.data_int}
                        onChange={onChange}
                    />
                    {errors.data_int && <p className="error">{errors.data_int[0]}</p>}
                </div>

                <button type="submit" disabled={isLoading}>
                    {isLoading ? 'Submitting...' : 'Submit'}
                </button>
            </form>

            {status && <p className="status">{status}</p>}
        </div>
    );
};

export default SignupFormPresentation;