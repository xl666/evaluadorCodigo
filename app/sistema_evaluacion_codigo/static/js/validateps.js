document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.querySelector('input[name="password"]');
    const confirmPasswordInput = document.querySelector('input[name="conf_password"]');
    const saveButton = document.getElementById('btn-save');
    const passwordHint = document.getElementById('password-hint');
    const requirementsList = document.getElementById('password-requirements');
    let hintShown = false;

    function validatePassword() {
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;
        const passwordRegex = /[!@#$%^&*()_\-+=\[\]{}|;:'",.<>?\/]/;

        // Show hint only when user starts typing
        if (password.length > 0 && !hintShown) {
            passwordHint.style.display = 'block';
            hintShown = true;
        }

        // Check if passwords match and meet criteria
        const passwordsMatch = password === confirmPassword;
        const passwordValid = passwordRegex.test(password);
        const passwordLenght = (password.length > 12)

        // Update requirements list
        if (passwordLenght) {
            document.getElementById('min-length').style.display = 'none';
        } else {
            document.getElementById('min-length').style.display = 'list-item';
        }

        if (passwordRegex.test(password)) {
            document.getElementById('special-char').style.display = 'none';
        } else {
            document.getElementById('special-char').style.display = 'list-item';
        }

        if (passwordsMatch) {
            document.getElementById('match').style.display = 'none';
        } else {
            document.getElementById('match').style.display = 'list-item';
        }

        // Enable or disable save button based on validation
        if (passwordsMatch && passwordValid && passwordLenght) {
            saveButton.disabled = false;
            hintShown = false;
            passwordHint.style.display = 'none';
        } else {
            saveButton.disabled = true;
            hintShown = true;
            passwordHint.style.display = 'block';
        }
    }

    passwordInput.addEventListener('input', validatePassword);
    confirmPasswordInput.addEventListener('input', validatePassword);
});
