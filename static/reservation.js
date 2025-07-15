document.getElementById("carDetailsForm").addEventListener("submit", function(event) {
    event.preventDefault();

    let carMake = document.getElementById("carMake").value;
    let carModel = document.getElementById("carModel").value;
    let carYear = document.getElementById("carYear").value;
    let carLicense = document.getElementById("carLicense").value;
    let slotNumber = "P1";  // Default value (isko dynamically set karna ho to modify karein)

    fetch("/reserve", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            slotNumber: slotNumber,
            carMake: carMake,
            carModel: carModel,
            carYear: carYear,
            carLicense: carLicense
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response:", data);  // Debugging ke liye console me print hoga
        if (data.message) {
            alert(data.message);
            window.location.href = "/parking";  // Success hone ke baad redirect karega
        } else {
            alert("Reservation failed: " + data.error);
        }
    })
    .catch(error => console.error("Error:", error));
});
