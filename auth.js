document.addEventListener('DOMContentLoaded', function() {
    const enterButton = document.querySelector('.enter-button');
    const initialsInput = document.getElementById('initials');

    if (enterButton && initialsInput) {
        // Add click handler for the Enter Site button
        enterButton.addEventListener('click', function() {
            const initials = initialsInput.value;
            if (initials && initials.length >= 2) {
                localStorage.setItem('authorized', 'true');
                localStorage.setItem('userInitials', initials);
                window.location.href = 'chatbot.html';
            } else {
                alert('Please enter your initials (minimum 2 characters)');
            }
        });

        // Add enter key handler
        initialsInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                enterButton.click();
            }
        });
    } else {
        // On other pages, check authorization
        if (!localStorage.getItem('authorized')) {
            window.location.href = 'auth.html';
        }
    }
});
