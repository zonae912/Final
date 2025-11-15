// AI Contribution: Copilot generated client-side JavaScript utilities
// Reviewed and approved by team

// CSRF token handling for AJAX requests
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
}

// Show loading spinner
function showLoading() {
    const overlay = document.createElement('div');
    overlay.className = 'spinner-overlay';
    overlay.innerHTML = '<div class="spinner-border text-light" role="status"><span class="visually-hidden">Loading...</span></div>';
    overlay.id = 'loading-overlay';
    document.body.appendChild(overlay);
}

// Hide loading spinner
function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.remove();
    }
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

// Client-side form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    return form.checkValidity();
}

// Confirm action
function confirmAction(message) {
    return confirm(message || 'Are you sure?');
}

// Auto-dismiss alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        if (!alert.classList.contains('alert-permanent')) {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });
});

// Image preview for file uploads
function previewImage(input, previewId) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById(previewId).src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// Rating stars interaction
function setRating(rating) {
    document.getElementById('rating').value = rating;
    const stars = document.querySelectorAll('.rating-star');
    stars.forEach((star, index) => {
        if (index < rating) {
            star.classList.add('text-warning');
            star.classList.remove('text-muted');
        } else {
            star.classList.add('text-muted');
            star.classList.remove('text-warning');
        }
    });
}

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Initialize popovers
document.addEventListener('DOMContentLoaded', function() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// Search with debounce
let searchTimeout;
function debounceSearch(searchFunction, delay = 300) {
    return function() {
        const context = this;
        const args = arguments;
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => searchFunction.apply(context, args), delay);
    };
}

// Booking availability checker
async function checkAvailability(resourceId, startDate, endDate) {
    try {
        const response = await fetch(
            `/bookings/api/check-availability/${resourceId}?start=${startDate}&end=${endDate}`
        );
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error checking availability:', error);
        return { available: false, message: 'Error checking availability' };
    }
}

console.log('Campus Resource Hub - Client-side scripts loaded');
