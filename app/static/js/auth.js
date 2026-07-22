// SECUREVISION — Auth JS (password strength, registration confirm)

document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('regPassword');
    const strengthBar = document.getElementById('strengthBar');
    const strengthLabel = document.getElementById('strengthLabel');

    if (passwordInput && strengthBar && strengthLabel) {
        passwordInput.addEventListener('input', function() {
            const password = this.value;
            const result = getPasswordStrength(password);
            strengthBar.style.width = result.percent + '%';
            strengthBar.style.background = result.color;
            strengthLabel.textContent = password ? result.label : 'Enter a password';
            strengthLabel.style.color = result.color;
        });
    }
});

function getPasswordStrength(password) {
    let score = 0;
    if (password.length >= 8) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[a-z]/.test(password)) score++;
    if (/\d/.test(password)) score++;
    if (/[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\;\'`~/]/.test(password)) score++;

    score = Math.min(score, 4);
    const labels = ['Very Weak', 'Weak', 'Fair', 'Strong', 'Very Strong'];
    const colors = ['#ef4444', '#f59e0b', '#3b82f6', '#22c55e', '#06b6d4'];

    return {
        score: score,
        label: labels[score],
        color: colors[score],
        percent: score * 25
    };
}

function confirmRegistration() {
    const btn = document.getElementById('confirmRegBtn');
    if (!btn) return;
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Creating Account...';

    fetch(CONFIRM_REG_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRF_TOKEN
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = data.redirect;
        } else {
            btn.disabled = false;
            btn.innerHTML = '<i class="bi bi-check-circle me-2"></i>Complete Registration';
            alert(data.message || 'Registration failed.');
        }
    })
    .catch(err => {
        btn.disabled = false;
        btn.innerHTML = '<i class="bi bi-check-circle me-2"></i>Complete Registration';
        alert('An error occurred. Please try again.');
    });
}
