document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('prescription-modal');
    const modalContent = modal.querySelector('.modal-content');
    const span = modal.querySelector('.close');
    const prescriptionNo = document.getElementById('prescription-no');
    const prescriptionDate = document.getElementById('prescription-date');
    const patientName = document.getElementById('patient-name');
    const patientAge = document.getElementById('patient-age');
    const patientPhone = document.getElementById('patient-phone');
    const patientDob = document.getElementById('patient-dob');
    const patientEmail = document.getElementById('patient-email');
    const patientGender = document.getElementById('patient-gender');
    const patientAddress = document.getElementById('patient-address');
    const patientAllergies = document.getElementById('patient-allergies');
    const patientHealthCondition = document.getElementById('patient-health-condition');
    const physicianName = document.getElementById('physician-name');
    const physicianPhone = document.getElementById('physician-phone');
    const physicianSignature = document.getElementById('physician-signature');
    const physicianEmail = document.getElementById('physician-email');

    document.querySelectorAll('.prescription-item').forEach(item => {
        item.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            // Fetch prescription details from the server or a data source
            // For demonstration, using static content
            prescriptionNo.textContent = `000${id}`;
            prescriptionDate.textContent = `September 28, 1977`;
            patientName.textContent = `Cherianne Gubbins`;
            patientAge.textContent = `10`;
            patientPhone.textContent = `+3 (66) 651-5527`;
            patientDob.textContent = `Wednesday, September 28, 1977`;
            patientEmail.textContent = `jtobias1@umich.edu`;
            patientGender.textContent = `Option 2`;
            patientAddress.textContent = `80776 Debs Drive, 15 Redwing Lane, Palmdale, California, 93591, United States`;
            patientAllergies.textContent = `Vestibulum rutrum rutrum neque.`;
            patientHealthCondition.textContent = `Nulla justo. Aliquam quis turpis eget elit sodales scelerisque. Mauris sit amet eros.`;
            physicianName.textContent = `Cherianne Gubbins`;
            physicianPhone.textContent = `+3 (66) 651-5527`;
            physicianSignature.innerHTML = `<img src="signature.png" alt="signature">`;
            physicianEmail.textContent = `jtobias1@umich.edu`;

            modal.style.display = 'block';
        });
    });

    span.onclick = function() {
        modal.style.display = 'none';
    }

    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    }
});
