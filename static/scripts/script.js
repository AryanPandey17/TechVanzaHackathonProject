const testDetails = {
    CBC: {
        name: 'Complete Blood Count (CBC)',
        description: 'A complete blood count (CBC) is a blood test used to evaluate your overall health and detect a wide range of disorders, including anemia, infection and leukemia.',
        price: '$50'
    },
    Lipid: {
        name: 'Lipid Profile',
        description: 'A lipid profile is a blood test that measures the levels of cholesterol and triglycerides in your blood. This test helps assess your risk of cardiovascular disease.',
        price: '$75'
    },
    Thyroid: {
        name: 'Thyroid Function Test',
        description: 'Thyroid function tests are blood tests that check how well your thyroid is working. They measure levels of thyroid hormones and help diagnose thyroid disorders.',
        price: '$85'
    },
    Electrolytes: {
        name: 'Electrolytes Panel',
        description: 'An electrolytes panel measures the levels of minerals in your blood, such as sodium, potassium, and chloride. It helps assess hydration status and kidney function.',
        price: '$40'
    },
    LiverPanel: {
        name: 'Liver Function Test',
        description: 'A liver function test checks various enzymes and proteins in your blood to assess liver health and detect liver diseases.',
        price: '$60'
    },
    DiabetesPanel: {
        name: 'Diabetes Panel',
        description: 'A diabetes panel includes tests like fasting glucose and HbA1c to evaluate blood sugar levels and diagnose diabetes or prediabetes.',
        price: '$70'
    },
    ComprehensiveMetabolicPanel: {
        name: 'Comprehensive Metabolic Panel (CMP)',
        description: 'The CMP is a group of tests that measure glucose, calcium, electrolytes, and kidney and liver function to provide a comprehensive overview of your metabolic health.',
        price: '$90'
    },
    ProthrombinTime: {
        name: 'Prothrombin Time (PT)',
        description: 'This test measures how long it takes for your blood to clot. It is used to monitor patients on anticoagulant therapy or to assess bleeding disorders.',
        price: '$50'
    },
    CReactiveProtein: {
        name: 'C-Reactive Protein (CRP) Test',
        description: 'The CRP test measures the level of C-reactive protein in your blood, which can indicate inflammation or infection in the body.',
        price: '$45'
    },
    VitaminDLevels: {
        name: 'Vitamin D Level Test',
        description: 'This test measures the level of vitamin D in your blood, which is essential for bone health and overall well-being.',
        price: '$55'
    }
};

document.querySelectorAll('[data-bs-toggle="modal"]').forEach(button => {
    button.addEventListener('click', (e) => {
        const testType = e.target.getAttribute('data-test');
        if (testType) {
            const test = testDetails[testType];
            document.getElementById('testDescription').innerHTML = `
                <h4>${test.name}</h4>
                <p>${test.description}</p>
                <p><strong>Price:</strong> ${test.price}</p>
            `;
            document.getElementById('selectedTest').innerHTML = `
                <p><strong>Test:</strong> ${test.name}</p>
                <p><strong>Price:</strong> ${test.price}</p>
            `;
        }
    });
});

document.getElementById('bookingForm').addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Booking submitted successfully!');
    bootstrap.Modal.getInstance(document.getElementById('bookingModal')).hide();
});