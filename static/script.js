// static/script.js
function searchNames() {
    const input = document.getElementById('searchInput').value.toLowerCase();
    const names = document.querySelectorAll('#namesList li');

    names.forEach(name => {
        const text = name.textContent.toLowerCase();
        if (text.includes(input)) {
            name.style.display = "";
        } else {
            name.style.display = "none";
        }
    });
}

// Sample JavaScript to handle form submission
document.getElementById('registration-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    const formData = new FormData(this);

    fetch('/submit', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Submission failed');
        }
    })
    .then(data => {
        // Redirect to the success page or show success message
        window.location.href = '/success'; // Change this to your success page route
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
