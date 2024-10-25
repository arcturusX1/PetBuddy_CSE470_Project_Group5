/* eslint-disable no-unused-vars */
// src/components/VetList.jsx
import React, { useState, useEffect } from 'react';

const VetList = () => {
  const [vets, setVets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchVets = async () => {
      try {
        setLoading(true);
        // Updated URL to match new API endpoint
        const response = await fetch('http://localhost:5000/api/vets');
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Received data:', data); // Debug log
        
        setVets(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching vets:', err);
        setError('Failed to fetch vets');
      } finally {
        setLoading(false);
      }
    };

    fetchVets();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!vets?.length) return <div>No veterinarians found.</div>;

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">Veterinarians</h2>
      <div className="grid gap-4">
        {vets.map((vet) => (
        //   <div key={vet.id} className="p-4 border rounded shadow">
        //     <h3 className="font-semibold">{vet.first_name}{vet.last_name}</h3>
        //     <p>Workplace: {vet.workplace}</p>
        //   </div>
          <ul key={vet.id}>
            <li>{vet.first_name} {vet.last_name} {vet.workplace}</li>
          </ul>
        ))}
      </div>
    </div>
  );
};

export default VetList;
