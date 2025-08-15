// Common JavaScript functionality for Kisan+

// Initialize speech recognition if available
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    window.recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    window.recognition.continuous = false;
    window.recognition.interimResults = false;
    window.recognition.lang = 'en-US';
}

// Text-to-speech functionality
function speakText(text) {
    if ('speechSynthesis' in window) {
        // Stop any ongoing speech
        speechSynthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-US';
        utterance.rate = 0.8;
        utterance.pitch = 1;
        utterance.volume = 1;
        
        speechSynthesis.speak(utterance);
    } else {
        console.log('Text-to-speech not supported');
    }
}

// Voice recognition functionality
function startVoiceRecognition(inputId, callback) {
    if (!window.recognition) {
        alert('Voice recognition not supported in this browser');
        return;
    }
    
    window.recognition.start();
    
    window.recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        const inputElement = document.getElementById(inputId);
        if (inputElement) {
            inputElement.value = transcript;
        }
        
        if (callback && typeof callback === 'function') {
            callback(transcript);
        }
    };
    
    window.recognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
    };
}

// Utility functions
const utils = {
    // Format currency
    formatCurrency: function(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR',
            maximumFractionDigits: 0
        }).format(amount);
    },
    
    // Format date
    formatDate: function(date) {
        return new Intl.DateTimeFormat('en-IN', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(new Date(date));
    },
    
    // Format time
    formatTime: function(date) {
        return new Intl.DateTimeFormat('en-IN', {
            hour: '2-digit',
            minute: '2-digit'
        }).format(new Date(date));
    },
    
    // Debounce function
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Show loading state
    showLoading: function(element, text = 'Loading...') {
        if (element) {
            element.innerHTML = `
                <i class="fas fa-spinner fa-spin mr-2"></i>
                ${text}
            `;
            element.disabled = true;
        }
    },
    
    // Hide loading state
    hideLoading: function(element, originalText) {
        if (element) {
            element.innerHTML = originalText;
            element.disabled = false;
        }
    },
    
    // Show notification
    showNotification: function(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 p-4 rounded-lg text-white z-50 ${
            type === 'success' ? 'bg-green-500' : 
            type === 'error' ? 'bg-red-500' : 
            type === 'warning' ? 'bg-yellow-500' : 'bg-blue-500'
        }`;
        notification.innerHTML = `
            <div class="flex items-center space-x-2">
                <i class="fas ${
                    type === 'success' ? 'fa-check-circle' : 
                    type === 'error' ? 'fa-exclamation-circle' : 
                    type === 'warning' ? 'fa-exclamation-triangle' : 'fa-info-circle'
                }"></i>
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" class="ml-2">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
    }
};

// Network status detection
function checkNetworkStatus() {
    if (navigator.onLine) {
        utils.showNotification('Internet connection restored', 'success');
    } else {
        utils.showNotification('Working offline - some features may be limited', 'warning');
    }
}

// Listen for network changes
window.addEventListener('online', checkNetworkStatus);
window.addEventListener('offline', checkNetworkStatus);

// Service Worker registration for offline support
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/static/sw.js')
            .then(function(registration) {
                console.log('ServiceWorker registration successful');
            })
            .catch(function(error) {
                console.log('ServiceWorker registration failed');
            });
    });
}

// Touch gesture support for mobile
function addTouchSupport() {
    let touchStartX = 0;
    let touchStartY = 0;
    
    document.addEventListener('touchstart', function(e) {
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
    });
    
    document.addEventListener('touchend', function(e) {
        if (!touchStartX || !touchStartY) return;
        
        const touchEndX = e.changedTouches[0].clientX;
        const touchEndY = e.changedTouches[0].clientY;
        const diffX = touchStartX - touchEndX;
        const diffY = touchStartY - touchEndY;
        
        // Horizontal swipe
        if (Math.abs(diffX) > Math.abs(diffY)) {
            if (diffX > 50) {
                // Swipe left
                document.dispatchEvent(new CustomEvent('swipeLeft'));
            } else if (diffX < -50) {
                // Swipe right
                document.dispatchEvent(new CustomEvent('swipeRight'));
            }
        }
        
        touchStartX = 0;
        touchStartY = 0;
    });
}

// Initialize touch support
addTouchSupport();

// Image compression for uploads
function compressImage(file, maxWidth = 800, quality = 0.8) {
    return new Promise((resolve) => {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();
        
        img.onload = function() {
            const ratio = Math.min(maxWidth / img.width, maxWidth / img.height);
            canvas.width = img.width * ratio;
            canvas.height = img.height * ratio;
            
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            
            canvas.toBlob(resolve, 'image/jpeg', quality);
        };
        
        img.src = URL.createObjectURL(file);
    });
}

// Local storage helpers
const storage = {
    set: function(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (e) {
            console.error('Error saving to localStorage:', e);
        }
    },
    
    get: function(key) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch (e) {
            console.error('Error reading from localStorage:', e);
            return null;
        }
    },
    
    remove: function(key) {
        try {
            localStorage.removeItem(key);
        } catch (e) {
            console.error('Error removing from localStorage:', e);
        }
    }
};

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    // Update time displays
    function updateTime() {
        const timeElements = document.querySelectorAll('.current-time');
        const now = new Date();
        timeElements.forEach(el => {
            el.textContent = utils.formatTime(now);
        });
    }
    
    updateTime();
    setInterval(updateTime, 60000); // Update every minute
    
    // Initialize tooltips
    const tooltipElements = document.querySelectorAll('[title]');
    tooltipElements.forEach(el => {
        el.addEventListener('mouseenter', function() {
            // Custom tooltip implementation can go here
        });
    });
    
    console.log('Kisan+ application initialized');
});
