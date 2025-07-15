onst cars = [
    { id: 1, name: 'Car A', details: 'Details about Car A' },
    { id: 2, name: 'Car B', details: 'Details about Car B' },
    { id: 3, name: 'Car C', details: 'Details about Car C' }
];

// Populate car list on Car Details Page
if (document.getElementById('carList')) {
    const carList = document.getElementById('carList');
    cars.forEach(car => {
        const carDiv = document.createElement('div');
        carDiv.classList.add('car');
        carDiv.innerHTML = `<h3>${car.name}</h3><p>${car.details}</p>`;
        carList.appendChild(carDiv);
    });
}

// Populate car options on Reservation Page
if (document.getElementById('carSelect')) {
    const carSelect = document.getElementById('carSelect');
    cars.forEach(car => {
        const option = document.createElement('option');
        option.value = car.id;
        option.textContent = car.name;
        carSelect.appendChild(option);
    });
}

// Handle login form submission
function handleLogin(event) {
    event.preventDefault();
    // Implement login logic here
    alert('Login successful');
    window.location.href = 'car_details.html';
}

// Handle reservation form submission
function handleReservation(event) {
    event.preventDefault();
    const carId = document.getElementById('carSelect').value;
    const reservationTime = document.getElementById('reservationTime').value;
    if (carId && reservationTime) {
        // Implement reservation logic here
        alert(`Reservation successful for ${cars.find(car => car.id == carId).name} at ${reservationTime}`);
       
::contentReference[oaicite:0]{index=0}
 


