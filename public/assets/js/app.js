// Initialize AOS (Animate On Scroll) and GSAP animations
document.addEventListener("DOMContentLoaded", function () {
  // Initialize AOS if available
  if (typeof AOS !== "undefined") {
    AOS.init({
      duration: 800,
      easing: "ease-in-out",
      once: true,
      offset: 100,
    });
  }

  // GSAP Animation for Hero Title
  if (typeof gsap !== "undefined") {
    const heroTitle = document.getElementById("heroTitle");
    if (heroTitle) {
      gsap.from(heroTitle, {
        duration: 1,
        y: 50,
        opacity: 0,
        ease: "power3.out",
      });
    }

    // Animate cards on hover
    const cards = document.querySelectorAll(".card");
    cards.forEach((card) => {
      card.addEventListener("mouseenter", function () {
        gsap.to(this, {
          duration: 0.3,
          y: -10,
          boxShadow: "0 15px 35px rgba(0, 0, 0, 0.2)",
          ease: "power2.out",
        });
      });

      card.addEventListener("mouseleave", function () {
        gsap.to(this, {
          duration: 0.3,
          y: 0,
          boxShadow: "0 0.125rem 0.25rem rgba(0, 0, 0, 0.075)",
          ease: "power2.out",
        });
      });
    });
  }

  // Add smooth scrolling to all links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });

  // Navbar scroll effect
  const navbar = document.querySelector(".navbar");
  if (navbar && navbar.classList.contains("sticky-top")) {
    window.addEventListener("scroll", function () {
      if (window.scrollY > 50) {
        navbar.classList.add("scrolled");
      } else {
        navbar.classList.remove("scrolled");
      }
    });
  }
});

// Helper: Show toast notification
function showToast(message, type = "success") {
  const toast = document.createElement("div");
  toast.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
  toast.style.zIndex = "9999";
  toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, 5000);
}

// Helper: Format date
function formatDate(dateString) {
  const options = {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  };
  return new Date(dateString).toLocaleDateString("id-ID", options);
}

// Helper: Validate email
function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

// Helper: Validate phone number (Indonesian format)
function validatePhone(phone) {
  const re = /^(\+62|62|0)[0-9]{9,12}$/;
  return re.test(phone.replace(/\s/g, ""));
}

// Helper: Debounce function
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Helper: API fetch wrapper
async function apiRequest(url, options = {}) {
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Request failed");
    }

    return data;
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
}

// Helper: Add loading state to buttons
function setButtonLoading(button, isLoading) {
  if (isLoading) {
    button.disabled = true;
    button.dataset.originalText = button.innerHTML;
    button.innerHTML =
      '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
  } else {
    button.disabled = false;
    button.innerHTML = button.dataset.originalText || button.innerHTML;
  }
}

// Helper: Robust image loading with fallback
function createImageWithFallback(src, alt, className = '', placeholderPath = '/assets/placeholder.svg') {
  const img = document.createElement('img');
  img.src = src;
  img.alt = alt;
  if (className) img.className = className;
  
  // Set up error handling to prevent infinite loops
  img.onerror = function() {
    // Prevent infinite loop by setting onerror to null
    this.onerror = null;
    console.warn(`Failed to load image: ${this.src}, using placeholder`);
    this.src = placeholderPath;
  };
  
  img.onload = function() {
    console.log(`Successfully loaded image: ${this.src}`);
  };
  
  return img;
}

// Helper: Set up image fallback for existing images
function setupImageFallback(imgElement, placeholderPath = '/assets/placeholder.svg') {
  if (!imgElement) return;
  
  // Store original src
  const originalSrc = imgElement.src;
  
  imgElement.onerror = function() {
    // Prevent infinite loop
    this.onerror = null;
    console.warn(`Failed to load image: ${originalSrc}, using placeholder`);
    this.src = placeholderPath;
  };
  
  imgElement.onload = function() {
    console.log(`Successfully loaded image: ${this.src}`);
  };
}

// Helper: Preload images with fallback
async function preloadImage(src, placeholderPath = '/assets/placeholder.svg') {
  return new Promise((resolve) => {
    const img = new Image();
    
    img.onload = () => {
      console.log(`Preloaded image: ${src}`);
      resolve(src);
    };
    
    img.onerror = () => {
      console.warn(`Failed to preload image: ${src}, using placeholder`);
      resolve(placeholderPath);
    };
    
    img.src = src;
  });
}

// Export functions for use in other scripts
window.appHelpers = {
  showToast,
  formatDate,
  validateEmail,
  validatePhone,
  debounce,
  apiRequest,
  setButtonLoading,
  createImageWithFallback,
  setupImageFallback,
  preloadImage,
};

console.log("App.js loaded successfully!");