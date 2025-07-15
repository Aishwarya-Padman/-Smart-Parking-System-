document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
  
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
  
    // Simple validation
    if (username === '' || password === '') {
      alert('Please fill in both fields.');
      return;
    }
  
    // For demonstration: hardcoded credentials
    const validUsername = 'user';
    const validPassword = 'password123';
  
    if (username === validUsername && password === validPassword) {
      alert('Login successful!');
      // Redirect to the reservation page
      window.location.href = 'reservation.html';
    } else {
      alert('Invalid credentials. Please try again.');
    }
  });