// SECUREVISION — Image Password JS

let selectedSequence = [];

// Registration: toggle image selection
function toggleImageSelect(card, imageId) {
    const idx = selectedSequence.indexOf(imageId);
    if (idx > -1) {
        // Remove
        selectedSequence.splice(idx, 1);
        card.classList.remove('selected');
    } else {
        if (selectedSequence.length >= 5) return;
        // Add
        selectedSequence.push(imageId);
        card.classList.add('selected');
    }
    updateSequenceDisplay();
    updateBadgeNumbers();
    updateConfirmButton();
}

function updateSequenceDisplay() {
    const display = document.getElementById('sequenceDisplay');
    const placeholder = document.getElementById('sequencePlaceholder');
    if (!display) return;

    // Clear all except placeholder
    display.querySelectorAll('.sequence-item').forEach(el => el.remove());

    if (selectedSequence.length === 0) {
        if (placeholder) placeholder.style.display = '';
        return;
    }
    if (placeholder) placeholder.style.display = 'none';

    selectedSequence.forEach(function(id, index) {
        const item = document.createElement('div');
        item.className = 'sequence-item';
        item.innerHTML = '<span class="seq-num">' + (index + 1) + '</span>' + id.charAt(0).toUpperCase() + id.slice(1);
        display.appendChild(item);
    });
}

function updateBadgeNumbers() {
    // Clear all badges
    document.querySelectorAll('.image-select-badge').forEach(b => b.textContent = '');
    // Set numbers
    selectedSequence.forEach(function(id, index) {
        const badge = document.getElementById('badge-' + id);
        if (badge) badge.textContent = index + 1;
    });
}

function updateConfirmButton() {
    const btn = document.getElementById('confirmImagePwBtn');
    if (!btn) return;
    btn.disabled = selectedSequence.length < 3;
}

function resetImageSelection() {
    selectedSequence = [];
    document.querySelectorAll('.image-select-card.selected').forEach(c => c.classList.remove('selected'));
    document.querySelectorAll('.image-select-badge').forEach(b => b.textContent = '');
    updateSequenceDisplay();
    updateConfirmButton();
}

// Confirm image password during registration
function confirmImagePassword() {
    const btn = document.getElementById('confirmImagePwBtn');
    if (!btn || selectedSequence.length < 3) return;

    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Saving...';

    fetch(CONFIRM_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRF_TOKEN
        },
        body: JSON.stringify({ images: selectedSequence })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = data.redirect;
        } else {
            btn.disabled = false;
            btn.innerHTML = 'Confirm Image Password <i class="bi bi-check-circle ms-2"></i>';
            alert(data.message || 'Error saving image password.');
        }
    })
    .catch(err => {
        btn.disabled = false;
        btn.innerHTML = 'Confirm Image Password <i class="bi bi-check-circle ms-2"></i>';
        alert('An error occurred.');
    });
}

// Save new image password (change image password page)
function saveImagePassword() {
    const btn = document.getElementById('confirmImagePwBtn');
    const resultDiv = document.getElementById('saveResult');
    if (!btn || selectedSequence.length < 3) return;

    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Saving...';

    fetch(SAVE_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRF_TOKEN
        },
        body: JSON.stringify({ images: selectedSequence })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (resultDiv) {
                resultDiv.innerHTML = '<div class="alert alert-success"><i class="bi bi-check-circle-fill me-2"></i>' + data.message + '</div>';
            }
            setTimeout(function() { window.location.reload(); }, 1500);
        } else {
            btn.disabled = false;
            btn.innerHTML = 'Save New Image Password <i class="bi bi-check-circle ms-2"></i>';
            if (resultDiv) {
                resultDiv.innerHTML = '<div class="alert alert-danger">' + data.message + '</div>';
            }
        }
    })
    .catch(err => {
        btn.disabled = false;
        btn.innerHTML = 'Save New Image Password <i class="bi bi-check-circle ms-2"></i>';
        alert('An error occurred.');
    });
}

// Verification mode (Level 2)
let verifySequence = [];

function toggleVerifyImage(card, imageId) {
    const idx = verifySequence.indexOf(imageId);
    if (idx > -1) {
        verifySequence.splice(idx, 1);
        card.classList.remove('selected');
    } else {
        verifySequence.push(imageId);
        card.classList.add('selected');
    }
    updateVerifyDisplay();
    updateVerifyButton();
}

function updateVerifyDisplay() {
    const display = document.getElementById('sequenceDisplay');
    const placeholder = document.getElementById('sequencePlaceholder');
    if (!display) return;

    display.querySelectorAll('.sequence-item').forEach(el => el.remove());

    if (verifySequence.length === 0) {
        if (placeholder) placeholder.style.display = '';
        return;
    }
    if (placeholder) placeholder.style.display = 'none';

    verifySequence.forEach(function(id, index) {
        const item = document.createElement('div');
        item.className = 'sequence-item';
        item.innerHTML = '<span class="seq-num">' + (index + 1) + '</span>' + id.charAt(0).toUpperCase() + id.slice(1);
        display.appendChild(item);
    });
}

function updateVerifyButton() {
    const btn = document.getElementById('submitVerifyBtn');
    if (!btn) return;
    btn.disabled = verifySequence.length < 3;
}

function resetVerifySequence() {
    verifySequence = [];
    document.querySelectorAll('.image-select-card.selected').forEach(c => c.classList.remove('selected'));
    updateVerifyDisplay();
    updateVerifyButton();
    const errDiv = document.getElementById('verifyError');
    if (errDiv) errDiv.classList.add('d-none');
}

function submitVerifySequence() {
    const btn = document.getElementById('submitVerifyBtn');
    const errDiv = document.getElementById('verifyError');
    if (!btn || verifySequence.length < 3) return;

    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Verifying...';

    fetch(VERIFY_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRF_TOKEN
        },
        body: JSON.stringify({ sequence: verifySequence })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = data.redirect;
        } else {
            btn.disabled = false;
            btn.innerHTML = 'Verify <i class="bi bi-shield-check ms-2"></i>';
            if (errDiv) {
                errDiv.textContent = data.message || 'Authentication failed.';
                errDiv.classList.remove('d-none');
            }
            resetVerifySequence();
        }
    })
    .catch(err => {
        btn.disabled = false;
        btn.innerHTML = 'Verify <i class="bi bi-shield-check ms-2"></i>';
        if (errDiv) {
            errDiv.textContent = 'An error occurred. Please try again.';
            errDiv.classList.remove('d-none');
        }
    });
}
